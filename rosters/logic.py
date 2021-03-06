"""Business logic."""

import datetime
import logging
import math
from collections import OrderedDict

from ortools.sat.python import cp_model
from django.contrib.auth import get_user_model

from .models import Leave, Role, Shift, ShiftRule, TimeSlot, Day


log = logging.getLogger("django")


class SolutionNotFeasible(Exception):
    """Exception for when there is no feasible solution."""

    pass


class TooManyStaff(Exception):
    """Exception for when there are too many staff."""

    pass


class RosterGenerator:
    """Roster generator."""

    def __init__(self, start_date):
        """Create starting conditions."""
        self.workers = get_user_model().objects.filter(available=True)
        self.shifts = Shift.objects.all().order_by("shift_type")
        self.num_days = Day.objects.count()
        self.date_range = [
            start_date.date(),
            start_date.date() + datetime.timedelta(days=self.num_days - 1),
        ]
        self.previous_date_range = [
            start_date.date() - datetime.timedelta(days=self.num_days),
            start_date.date() - datetime.timedelta(days=1),
        ]
        self.leaves = Leave.objects.filter(date__range=self.date_range)
        self.dates = [
            (start_date + datetime.timedelta(days=n)).date()
            for n in range(self.num_days)
        ]
        self.extended_dates = [
            (
                start_date
                - datetime.timedelta(days=self.num_days)
                + datetime.timedelta(days=n)
            ).date()
            for n in range(2 * self.num_days)
        ]
        self.model = cp_model.CpModel()
        self.complete = False

    def _clear_existing_timeslots(self):
        # Delete existing timeslots in date range
        TimeSlot.objects.filter(date__range=self.date_range).delete()

    def _create_timeslots(self):
        # Create timeslots
        for day, date in enumerate(self.dates):
            for shift in self.shifts:
                day_group_days = shift.day_group.daygroupday_set.all()
                for day_group_day in day_group_days:
                    if day_group_day.day.number == day + 1:
                        TimeSlot.objects.create(date=date, shift=shift)
        self.timeslots = TimeSlot.objects.filter(date__range=self.date_range)

    def _check_if_too_many_staff(self):
        # Check if too many staff
        log.info("Too many staff check started...")
        total_staff_shifts = 0
        for worker in self.workers:
            leave_days = self.leaves.filter(staff_member=worker).count()
            if leave_days > worker.shifts_per_roster:
                total_staff_shifts += 0
            else:
                total_staff_shifts += worker.shifts_per_roster - leave_days
        total_shifts = 0
        for timeslot in self.timeslots:
            total_shifts += timeslot.shift.max_staff
        log.info("Total staff shifts: " + str(total_staff_shifts))
        log.info("Total shifts: " + str(total_shifts))
        if total_staff_shifts > total_shifts:
            log.info("Error: there are too many staff...")
            raise TooManyStaff("Too many staff.")
        log.info("Too many staff check completed...")

    def _collect_shift_requests(self):
        # Collect shift requests into friendly data structure
        log.info("Shift request collection started...")
        self.shift_requests = []
        for worker in self.workers:
            worker_shift_requests = []
            staffrequests = worker.staffrequest_set.all()
            for date in self.dates:
                worker_shift_requests_for_day = []
                for timeslot in TimeSlot.objects.filter(date=date).order_by(
                    "shift__shift_type"
                ):
                    priority = 0
                    for staffrequest in staffrequests:
                        if (
                            staffrequest.date == date
                            and staffrequest.shift == timeslot.shift
                        ):
                            if staffrequest.like:
                                priority = staffrequest.priority
                            else:
                                priority = -staffrequest.priority
                    worker_shift_requests_for_day.append(priority)
                worker_shift_requests.append(worker_shift_requests_for_day)
            self.shift_requests.append(worker_shift_requests)
        log.info("Shift request collection completed...")
        log.debug(self.shift_requests)

    def _create_shift_vars(self):
        """Create shift variables.

        shift_vars[(n, r, d, t)]:
        worker 'n' with role 'r' works on date 'd' in timeslot 't'
        """
        log.info("Shift variable creation started...")
        self.shift_vars = {}
        for worker in self.workers:
            for role in worker.roles.all():
                for date in self.dates:
                    for timeslot in self.timeslots.filter(date=date).order_by(
                        "shift__shift_type"
                    ):
                        n = worker.id
                        r = role.id
                        d = date
                        t = timeslot.id
                        self.shift_vars[(n, r, d, t)] = self.model.NewBoolVar(
                            f"shift_n{n}r{r}d{d}t{t}"
                        )
        log.info("Shift variable creation completed...")
        log.debug(self.shift_vars.keys())

    def _create_previous_shift_vars(self):
        # Create shift variables and fixed constraints
        # for previous roster period
        log.info("Creation of shift variables for previous period started...")
        previous_timeslots = TimeSlot.objects.filter(
            date__range=self.previous_date_range
        )
        for timeslot in previous_timeslots:
            for worker in timeslot.staff.all():
                n = worker.id
                r = worker.roles.all()[0]
                d = timeslot.date
                t = timeslot.id
                self.shift_vars[(n, r, d, t)] = self.model.NewBoolVar(
                    f"shift_n{n}r{r}d{d}t{t}"
                )
                self.model.Add(self.shift_vars[(n, r, d, t)] == 1)
        log.info(
            "Creation of shift variables for previous period completed..."
        )

    def _exclude_leave_dates(self):
        # Exclude leave dates from roster
        log.info("Exclusion of leave dates started...")
        for timeslot in self.timeslots:
            for leave in self.leaves:
                if timeslot.date == leave.date:
                    for role in leave.staff_member.roles.all():
                        self.model.Add(
                            self.shift_vars[
                                (
                                    leave.staff_member.id,
                                    role.id,
                                    timeslot.date,
                                    timeslot.id,
                                )
                            ]
                            == 0
                        )
        log.info("Exclusion of leave dates completed...")

    def _get_timeslot_ids(self):
        """Map date and shift to timeslot ID."""
        timeslot_ids = {}
        for date in self.extended_dates:
            timeslot_ids[date] = {}
            for shift in self.shifts:
                try:
                    timeslot_ids[date][shift] = TimeSlot.objects.get(
                        date=date, shift=shift
                    ).id
                except TimeSlot.DoesNotExist:
                    continue
        return timeslot_ids

    def _get_invalid_shift_seq(self, staff_rule):
        """Create invalid shift sequence for each rule.

        Example: { 1: [ "E", "L", "N"], 2: ["E", "L"] }
        """
        invalid_shift_sequence = OrderedDict()
        staff_rule_shifts = staff_rule.staffruleshift_set.all()
        staff_rule_shifts = staff_rule_shifts.order_by("position")
        for staff_rule_shift in staff_rule_shifts:
            invalid_shift_sequence.setdefault(
                staff_rule_shift.position, []
            ).append(staff_rule_shift.shift)
        return invalid_shift_sequence

    def _get_work_days_in_seq(self, invalid_shift_seq):
        """Get number of working days in invalid shift sequence."""
        work_days_in_seq = 0
        for position in invalid_shift_seq:
            if invalid_shift_seq[position][0] is not None:
                work_days_in_seq += 1
        return work_days_in_seq

    def _get_all_days_in_seq(self, staff_rule):
        """Get number of days in staff rule."""
        day_group_day_set = staff_rule.day_group.daygroupday_set.all()
        all_days_in_seq = [
            day_group_day.day.number for day_group_day in day_group_day_set
        ]
        return all_days_in_seq

    def _get_shift_vars_in_seq_off(
        self, date, invalid_shift_seq, roles, worker,
    ):
        """Find non-working shift variables in invalid sequence."""
        shift_vars_in_seq_off = []
        for day_num in invalid_shift_seq:
            if invalid_shift_seq[day_num][0] is None:
                day_to_test = date + datetime.timedelta(days=day_num - 1)
                for role in roles:
                    try:
                        for timeslot in self.timeslots.filter(
                            date=day_to_test
                        ):
                            shift_vars_in_seq_off.append(
                                self.shift_vars[
                                    (
                                        worker.id,
                                        role.id,
                                        day_to_test,
                                        timeslot.id,
                                    )
                                ]
                            )
                    except KeyError:
                        continue
        return shift_vars_in_seq_off

    def _get_shift_vars_in_seq_on(
        self,
        date,
        invalid_shift_seq,
        all_days_in_seq,
        roles,
        worker,
        timeslot_ids,
    ):
        """Find working day shift variables in invalid sequence."""
        shift_vars_in_seq_on = []
        for day_num in invalid_shift_seq:
            for invalid_shift in invalid_shift_seq[day_num]:
                day_to_test = date + datetime.timedelta(days=day_num - 1)

                # Skip if day not in day group for sequence
                delta = (day_to_test - self.dates[0]).days
                if delta < 0:
                    day_group_day_num = delta + self.num_days + 1
                else:
                    day_group_day_num = delta + 1
                if day_group_day_num not in all_days_in_seq:
                    break

                for role in roles:
                    try:
                        shift_vars_in_seq_on.append(
                            self.shift_vars[
                                (
                                    worker.id,
                                    role.id,
                                    day_to_test,
                                    timeslot_ids[day_to_test][invalid_shift],
                                )
                            ]
                        )
                    except KeyError:
                        continue
        return shift_vars_in_seq_on

    def _enforce_shift_sequences(self):
        """Enforce shift sequences / staff rules.

        Need to look at previous roster period also
        """
        log.info("Addition of shift sequence rules started...")

        timeslot_ids = self._get_timeslot_ids()

        for worker in self.workers:
            roles = worker.roles.all()
            for staff_rule in worker.staffrule_set.all():
                invalid_shift_seq = self._get_invalid_shift_seq(staff_rule)
                work_days_in_seq = self._get_work_days_in_seq(
                    invalid_shift_seq
                )
                all_days_in_seq = self._get_all_days_in_seq(staff_rule)

                for date in self.extended_dates:
                    shift_vars_in_seq_off = self._get_shift_vars_in_seq_off(
                        date, invalid_shift_seq, roles, worker,
                    )
                    shift_vars_in_seq_on = self._get_shift_vars_in_seq_on(
                        date,
                        invalid_shift_seq,
                        all_days_in_seq,
                        roles,
                        worker,
                        timeslot_ids,
                    )

                    # Apply constraints
                    if len(shift_vars_in_seq_off) == 0:
                        self.model.Add(
                            sum(shift_vars_in_seq_on) < work_days_in_seq
                        )
                    else:
                        for item, var in enumerate(shift_vars_in_seq_off):
                            shift_vars_in_seq_off[item] = var.Not()
                        self.model.Add(
                            sum(shift_vars_in_seq_on) < work_days_in_seq
                        ).OnlyEnforceIf(shift_vars_in_seq_off)
        log.info("Addition of shift sequence rules completed...")

    def _collect_skill_mix_rules(self):
        """Collect shift rules into friendly structure."""
        log.info("Collection of skill mix rules started...")
        self.shift_rules = {}
        for shift in self.shifts:
            self.shift_rules[shift.id] = []
            shiftrules = ShiftRule.objects.filter(shift=shift)
            for shiftrule in shiftrules:
                shiftruleroles = shiftrule.shiftrulerole_set.all()
                role_count = {}
                for role in Role.objects.all():
                    role_count[role.id] = 0
                for shiftrulerole in shiftruleroles:
                    role_count[shiftrulerole.role.id] = shiftrulerole.count
                self.shift_rules[shift.id].append(role_count)
        log.info("Collection of skill mix rules completed...")
        log.debug(self.shift_rules)

    def _create_intermediate_skill_mix_vars(self):
        # Intermediate shift rule variables
        log.info("Creation of skill mix intermediate variables started...")
        self.intermediate_skill_mix_vars = {
            (timeslot.id, rule_num): self.model.NewBoolVar(
                f"t{timeslot.id}r{rule_num}"
            )
            for timeslot in self.timeslots
            for rule_num, rule in enumerate(
                self.shift_rules[timeslot.shift.id]
            )
        }
        log.info("Creation of skill mix intermediate variables completed...")
        log.debug(self.intermediate_skill_mix_vars)

    def _enforce_one_skill_mix_rule_at_a_time(self):
        """Only one skill mix rule at a time should be enforced."""
        log.info("Enforcement of one shift rule at a time started...")
        for timeslot in self.timeslots:
            if len(self.shift_rules[timeslot.shift.id]) >= 1:
                self.model.Add(
                    sum(
                        self.intermediate_skill_mix_vars[
                            (timeslot.id, rule_num)
                        ]
                        for rule_num, rule in enumerate(
                            self.shift_rules[timeslot.shift.id]
                        )
                    )
                    == 1
                )
        log.info("Enforcement of one shift rule at a time completed...")

    def _enforce_skill_mix_rules(self):
        """Enforce one skill mix rule per shift per timeslot."""
        log.info("Enforcement of skill mix rules started...")
        for shift_id in self.shift_rules:
            if len(self.shift_rules[shift_id]) >= 1:
                for rule_num, rule in enumerate(self.shift_rules[shift_id]):
                    for role_id in rule:
                        role_count = rule[role_id]
                        for timeslot in self.timeslots.filter(
                            shift__id=shift_id
                        ):
                            self.model.Add(
                                sum(
                                    self.shift_vars[
                                        (
                                            worker.id,
                                            role_id,
                                            timeslot.date,
                                            timeslot.id,
                                        )
                                    ]
                                    for worker in self.workers.filter(
                                        roles__id=role_id
                                    )
                                )
                                == role_count
                            ).OnlyEnforceIf(
                                self.intermediate_skill_mix_vars[
                                    (timeslot.id, rule_num)
                                ]
                            )
        log.info("Enforcement of skill mix rules completed...")

    def _enforce_one_shift_per_day(self):
        """Assign at most one shift per day per worker."""
        log.info("Restriction of staff to one shift per day started...")
        for worker in self.workers:
            for date in self.dates:
                if worker.shifts_per_roster != 0:  # Zero is unlimited shifts
                    self.model.Add(
                        sum(
                            self.shift_vars[
                                (worker.id, role.id, date, timeslot.id)
                            ]
                            for role in worker.roles.all()
                            for timeslot in TimeSlot.objects.filter(
                                date=date
                            ).order_by("shift__shift_type")
                        )
                        <= 1
                    )
        log.info("Restriction of staff to one shift per day completed...")

    def _get_shifts_per_roster(self, worker):
        """Get number of shifts to work in roster period."""
        leave_days = self.leaves.filter(staff_member=worker).count()
        work_fraction = 1 - (leave_days / self.num_days)
        shifts_per_roster = work_fraction * worker.shifts_per_roster
        if worker.max_shifts:
            shifts_per_roster = math.ceil(shifts_per_roster)
        else:
            shifts_per_roster = math.floor(shifts_per_roster)
        return shifts_per_roster

    def _enforce_shifts_per_roster(self):
        """Enforce shifts per roster for each worker."""
        log.info("Enforcement of shifts per roster started...")
        for worker in self.workers:
            num_shifts_worked = sum(
                self.shift_vars[(worker.id, role.id, date, timeslot.id)]
                for role in worker.roles.all()
                for date in self.dates
                for timeslot in TimeSlot.objects.filter(date=date).order_by(
                    "shift__shift_type"
                )
            )
            if worker.shifts_per_roster != 0:  # Zero means unlimited shifts
                shifts_per_roster = self._get_shifts_per_roster(worker)
                self.model.Add(num_shifts_worked == shifts_per_roster)
        log.info("Enforcement of shifts per roster completed...")

    def _split_list(self, alist, wanted_parts=1):
        """Split list into parts."""
        length = len(alist)
        return [
            alist[
                i * length // wanted_parts : (i + 1) * length // wanted_parts
            ]
            for i in range(wanted_parts)
        ]

    def _enforce_balanced_shifts(self):
        """Enforce balanced shifts for each worker."""
        log.info("Enforcement of balanced shifts started...")
        for worker in self.workers:
            leave_dates = [
                leave.date for leave in self.leaves.filter(staff_member=worker)
            ]
            dates = [date for date in self.dates if date not in leave_dates]
            dates1, dates2 = self._split_list(dates, wanted_parts=2)
            num_shifts_worked1 = sum(
                self.shift_vars[(worker.id, role.id, date, timeslot.id)]
                for role in worker.roles.all()
                for date in dates1
                for timeslot in TimeSlot.objects.filter(date=date).order_by(
                    "shift__shift_type"
                )
            )
            if worker.shifts_per_roster != 0:  # Zero means unlimited shifts
                shifts_per_roster = self._get_shifts_per_roster(worker)
                num_shifts = shifts_per_roster // 2
                if shifts_per_roster % 2 == 0:
                    self.model.Add(num_shifts_worked1 == num_shifts)
                else:
                    self.model.Add(num_shifts_worked1 == num_shifts + 1)
        log.info("Enforcement of balanced shifts completed...")

    def _maximise_staff_requests(self):
        """Maximise the number of satisfied staff requests."""
        log.info("Maximising of staff requests started...")
        self.model.Maximize(
            sum(
                self.shift_requests[n][d][s]
                * self.shift_vars[(worker.id, role.id, date, timeslot.id)]
                for n, worker in enumerate(self.workers)
                for role in worker.roles.all()
                for d, date in enumerate(self.dates)
                for s, timeslot in enumerate(
                    TimeSlot.objects.filter(date=date).order_by(
                        "shift__shift_type"
                    )
                )
            )
        )
        log.info("Maximising of staff requests completed...")

    def _solve_roster(self):
        """Create the solver and solve."""
        self.solver = cp_model.CpSolver()
        self.solver.parameters.max_time_in_seconds = 120
        log.info("Solver started...")
        solution_status = self.solver.Solve(self.model)
        log.info("Solver finished...")
        if solution_status == cp_model.INFEASIBLE:
            log.info("Solution is INFEASIBLE")
        if solution_status == cp_model.MODEL_INVALID:
            log.info("Solution is MODEL_INVALID")
        if solution_status == cp_model.UNKNOWN:
            log.info("Solution is UNKNOWN")
        if (
            solution_status != cp_model.FEASIBLE
            and solution_status != cp_model.OPTIMAL
        ):
            log.info("No feasible solution, raising exception...")
            raise SolutionNotFeasible("No feasible solutions.")

    def _populate_roster(self):
        """Poulate roster."""
        log.info("Population of roster started...")
        for d, date in enumerate(self.dates):
            for n, worker in enumerate(self.workers):
                for role in worker.roles.all():
                    for s, timeslot in enumerate(
                        TimeSlot.objects.filter(date=date).order_by(
                            "shift__shift_type"
                        )
                    ):
                        if (
                            self.solver.Value(
                                self.shift_vars[
                                    (worker.id, role.id, date, timeslot.id)
                                ]
                            )
                            == 1
                        ):
                            TimeSlot.objects.get(
                                date=date, shift=timeslot.shift
                            ).staff.add(worker)
                            if self.shift_requests[n][d][s] > 0:
                                log.info(
                                    f"Request Successful: "
                                    f"{worker.last_name}, {worker.first_name}"
                                    f" {role.role_name}"
                                    f" requested shift"
                                    f" {timeslot.shift.shift_type}"
                                    f" on"
                                    f" {timeslot.date}"
                                    f" and was assigned."
                                )
                            elif self.shift_requests[n][d][s] < 0:
                                log.info(
                                    f"Request Failed: "
                                    f"{worker.last_name}, {worker.first_name}"
                                    f" {role.role_name}"
                                    f" requested not to work shift"
                                    f" {timeslot.shift.shift_type}"
                                    f" on"
                                    f" {timeslot.date}"
                                    f" but was assigned."
                                )
                        else:
                            if self.shift_requests[n][d][s] > 0:
                                log.info(
                                    f"Request Failed: "
                                    f"{worker.last_name}, {worker.first_name}"
                                    f" {role.role_name}"
                                    f" requested shift"
                                    f" {timeslot.shift.shift_type}"
                                    f" on"
                                    f" {timeslot.date}"
                                    f" but was not assigned."
                                )
                            elif self.shift_requests[n][d][s] < 0:
                                log.info(
                                    f"Request Succeeded: "
                                    f"{worker.last_name}, {worker.first_name}"
                                    f" {role.role_name}"
                                    f" requested not to work shift"
                                    f" {timeslot.shift.shift_type}"
                                    f" on"
                                    f" {timeslot.date}"
                                    f" and was not assigned."
                                )
        log.info("Population of roster completed...")

    def create(self):
        """Create roster as per constraints."""
        self._clear_existing_timeslots()
        self._create_timeslots()
        self._check_if_too_many_staff()
        self._collect_shift_requests()
        self._create_shift_vars()
        self._create_previous_shift_vars()
        self._exclude_leave_dates()
        self._enforce_shift_sequences()
        self._collect_skill_mix_rules()
        self._create_intermediate_skill_mix_vars()
        self._enforce_one_skill_mix_rule_at_a_time()
        self._enforce_skill_mix_rules()
        self._enforce_one_shift_per_day()
        self._enforce_shifts_per_roster()
        self._enforce_balanced_shifts()
        self._maximise_staff_requests()
        self._solve_roster()
        self._populate_roster()
        self.complete = True


def get_roster_by_staff(start_date):
    """Create data structures for roster grouped by staff."""
    dates = []
    roster = OrderedDict()
    workers = (
        get_user_model()
        .objects.all()
        .order_by("roles__role_name", "last_name", "first_name")
    )
    num_days = Day.objects.count()
    for worker in workers:
        roster[worker.last_name + ", " + worker.first_name] = OrderedDict()
        staff_roles = ""
        for role in worker.roles.all().order_by("role_name"):
            staff_roles += role.role_name + " "
        roster[worker.last_name + ", " + worker.first_name][
            "roles"
        ] = staff_roles
        roster[worker.last_name + ", " + worker.first_name][
            "shifts_per_roster"
        ] = worker.shifts_per_roster
        leaves = Leave.objects.filter(staff_member=worker)
        dates = []
        for day in range(num_days):
            date = start_date + datetime.timedelta(days=day)
            date = date.date()
            dates.append(date)
            try:
                roster[worker.last_name + ", " + worker.first_name][
                    date
                ] = TimeSlot.objects.get(
                    date=date, staff=worker.id
                ).shift.shift_type
            except TimeSlot.DoesNotExist:
                leave = leaves.filter(date=date).count()
                if leave == 0:
                    roster[worker.last_name + ", " + worker.first_name][
                        date
                    ] = "X"
                else:
                    roster[worker.last_name + ", " + worker.first_name][
                        date
                    ] = leaves.get(date=date).description
            except TimeSlot.MultipleObjectsReturned:
                timeslots = TimeSlot.objects.filter(date=date, staff=worker.id)
                roster[worker.last_name + ", " + worker.first_name][date] = ""
                for timeslot in timeslots:
                    roster[worker.last_name + ", " + worker.first_name][
                        date
                    ] += (timeslot.shift.shift_type + " ")
    return dates, roster

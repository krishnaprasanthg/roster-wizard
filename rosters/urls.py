"""URLs."""

from django.urls import path

from .views import (
    LeaveListView,
    LeaveUpdateView,
    LeaveDetailView,
    LeaveDeleteView,
    LeaveCreateView,
    RoleListView,
    RoleUpdateView,
    RoleDetailView,
    RoleDeleteView,
    RoleCreateView,
    ShiftListView,
    ShiftUpdateView,
    ShiftDetailView,
    ShiftDeleteView,
    ShiftCreateView,
    ShiftRuleListView,
    ShiftRuleUpdateView,
    ShiftRuleDetailView,
    ShiftRuleDeleteView,
    ShiftRuleCreateView,
    ShiftRuleRoleListView,
    ShiftRuleRoleUpdateView,
    ShiftRuleRoleDetailView,
    ShiftRuleRoleDeleteView,
    ShiftRuleRoleCreateView,
    StaffRuleListView,
    StaffRuleUpdateView,
    StaffRuleDetailView,
    StaffRuleDeleteView,
    StaffRuleCreateView,
    StaffRuleShiftListView,
    StaffRuleShiftUpdateView,
    StaffRuleShiftDetailView,
    StaffRuleShiftDeleteView,
    StaffRuleShiftCreateView,
    TimeSlotListView,
    TimeSlotUpdateView,
    TimeSlotDetailView,
    TimeSlotDeleteView,
    TimeSlotCreateView,
    GenerateRosterView,
    SelectRosterView,
    RosterListView,
    StaffRequestListView,
    StaffRequestDeleteView,
    StaffRequestCreateView,
    StaffRequestUpdateView,
    StaffRequestDetailView,
    download_csv,
    DayGroupListView,
    DayGroupUpdateView,
    DayGroupDetailView,
    DayGroupDeleteView,
    DayGroupCreateView,
    DayGroupDayListView,
    DayGroupDayUpdateView,
    DayGroupDayDetailView,
    DayGroupDayDeleteView,
    DayGroupDayCreateView,
    DayListView,
    DayUpdateView,
    DayDetailView,
    DayDeleteView,
    DayCreateView,
    DaySetCreateView,
)

urlpatterns = [
    path(
        "leave/<int:pk>/update/",
        LeaveUpdateView.as_view(),
        name="leave_update",
    ),
    path("leave/<int:pk>/", LeaveDetailView.as_view(), name="leave_detail"),
    path(
        "leave/<int:pk>/delete/",
        LeaveDeleteView.as_view(),
        name="leave_delete",
    ),
    path("leave/create/", LeaveCreateView.as_view(), name="leave_create"),
    path("leave/", LeaveListView.as_view(), name="leave_list"),
    path(
        "role/<int:pk>/update/", RoleUpdateView.as_view(), name="role_update"
    ),
    path("role/<int:pk>/", RoleDetailView.as_view(), name="role_detail"),
    path(
        "role/<int:pk>/delete/", RoleDeleteView.as_view(), name="role_delete"
    ),
    path("role/create/", RoleCreateView.as_view(), name="role_create"),
    path("role/", RoleListView.as_view(), name="role_list"),
    path(
        "shift/<int:pk>/update/",
        ShiftUpdateView.as_view(),
        name="shift_update",
    ),
    path("shift/<int:pk>/", ShiftDetailView.as_view(), name="shift_detail"),
    path(
        "shift/<int:pk>/delete/",
        ShiftDeleteView.as_view(),
        name="shift_delete",
    ),
    path("shift/create/", ShiftCreateView.as_view(), name="shift_create"),
    path("shift/", ShiftListView.as_view(), name="shift_list"),
    path(
        "shiftrule/<int:pk>/update/",
        ShiftRuleUpdateView.as_view(),
        name="shift_rule_update",
    ),
    path(
        "shiftrule/<int:pk>/",
        ShiftRuleDetailView.as_view(),
        name="shift_rule_detail",
    ),
    path(
        "shiftrule/<int:pk>/delete/",
        ShiftRuleDeleteView.as_view(),
        name="shift_rule_delete",
    ),
    path(
        "shiftrule/create/",
        ShiftRuleCreateView.as_view(),
        name="shift_rule_create",
    ),
    path("shiftrule/", ShiftRuleListView.as_view(), name="shift_rule_list"),
    path(
        "shiftrulerole/<int:pk>/update/",
        ShiftRuleRoleUpdateView.as_view(),
        name="shift_rule_role_update",
    ),
    path(
        "shiftrulerole/<int:pk>/",
        ShiftRuleRoleDetailView.as_view(),
        name="shift_rule_role_detail",
    ),
    path(
        "shiftrulerole/<int:pk>/delete/",
        ShiftRuleRoleDeleteView.as_view(),
        name="shift_rule_role_delete",
    ),
    path(
        "shiftrulerole/<int:shiftrule>/create/",
        ShiftRuleRoleCreateView.as_view(),
        name="shift_rule_role_create",
    ),
    path(
        "shiftrulerole/",
        ShiftRuleRoleListView.as_view(),
        name="shift_rule_role_list",
    ),
    path(
        "staffrule/<int:pk>/update/",
        StaffRuleUpdateView.as_view(),
        name="staff_rule_update",
    ),
    path(
        "staffrule/<int:pk>/",
        StaffRuleDetailView.as_view(),
        name="staff_rule_detail",
    ),
    path(
        "staffrule/<int:pk>/delete/",
        StaffRuleDeleteView.as_view(),
        name="staff_rule_delete",
    ),
    path(
        "staffrule/create/",
        StaffRuleCreateView.as_view(),
        name="staff_rule_create",
    ),
    path("staffrule/", StaffRuleListView.as_view(), name="staff_rule_list"),
    path(
        "staffruleshift/<int:pk>/update/",
        StaffRuleShiftUpdateView.as_view(),
        name="staff_rule_shift_update",
    ),
    path(
        "staffruleshift/<int:pk>/",
        StaffRuleShiftDetailView.as_view(),
        name="staff_rule_shift_detail",
    ),
    path(
        "staffruleshift/<int:pk>/delete/",
        StaffRuleShiftDeleteView.as_view(),
        name="staff_rule_shift_delete",
    ),
    path(
        "staffruleshift/<int:staffrule>/create/",
        StaffRuleShiftCreateView.as_view(),
        name="staff_rule_shift_create",
    ),
    path(
        "staffruleshift/",
        StaffRuleShiftListView.as_view(),
        name="staff_rule_shift_list",
    ),
    path(
        "timeslot/<int:pk>/update/",
        TimeSlotUpdateView.as_view(),
        name="timeslot_update",
    ),
    path(
        "timeslot/<int:pk>/",
        TimeSlotDetailView.as_view(),
        name="timeslot_detail",
    ),
    path(
        "timeslot/<int:pk>/delete/",
        TimeSlotDeleteView.as_view(),
        name="timeslot_delete",
    ),
    path(
        "timeslot/create/",
        TimeSlotCreateView.as_view(),
        name="timeslot_create",
    ),
    path("timeslot/", TimeSlotListView.as_view(), name="timeslot_list"),
    path(
        "timeslot/generate",
        GenerateRosterView.as_view(),
        name="generate_roster",
    ),
    path("timeslot/select", SelectRosterView.as_view(), name="select_roster"),
    path("roster/", RosterListView.as_view(), name="roster_list"),
    path("roster/download", download_csv, name="download_csv"),
    path("daygroup/", DayGroupListView.as_view(), name="day_group_list"),
    path(
        "daygroup/<int:pk>/update/",
        DayGroupUpdateView.as_view(),
        name="day_group_update",
    ),
    path(
        "daygroup/<int:pk>/",
        DayGroupDetailView.as_view(),
        name="day_group_detail",
    ),
    path(
        "daygroup/<int:pk>/delete/",
        DayGroupDeleteView.as_view(),
        name="day_group_delete",
    ),
    path(
        "daygroup/create/",
        DayGroupCreateView.as_view(),
        name="day_group_create",
    ),
    path(
        "daygroupday/",
        DayGroupDayListView.as_view(),
        name="day_group_day_list",
    ),
    path(
        "daygroupday/<int:pk>/update/",
        DayGroupDayUpdateView.as_view(),
        name="day_group_day_update",
    ),
    path(
        "daygroupday/<int:pk>/",
        DayGroupDayDetailView.as_view(),
        name="day_group_day_detail",
    ),
    path(
        "daygroupday/<int:pk>/delete/",
        DayGroupDayDeleteView.as_view(),
        name="day_group_day_delete",
    ),
    path(
        "daygroupday/<int:daygroup>/create/",
        DayGroupDayCreateView.as_view(),
        name="day_group_day_create",
    ),
    path(
        "daygroupday/",
        DayGroupDayListView.as_view(),
        name="day_group_day_list",
    ),
    path("day/<int:pk>/update/", DayUpdateView.as_view(), name="day_update"),
    path("day/<int:pk>/", DayDetailView.as_view(), name="day_detail"),
    path("day/<int:pk>/delete/", DayDeleteView.as_view(), name="day_delete"),
    path("day/create/", DayCreateView.as_view(), name="day_create"),
    path("day/", DayListView.as_view(), name="day_list"),
    path("dayset/create", DaySetCreateView.as_view(), name="day_set_create"),
    path(
        "staff_request/<int:pk>/delete/",
        StaffRequestDeleteView.as_view(),
        name="staff_request_delete",
    ),
    path(
        "staff_request/create/",
        StaffRequestCreateView.as_view(),
        name="staff_request_create",
    ),
    path(
        "staff_request/",
        StaffRequestListView.as_view(),
        name="staff_request_list",
    ),
    path(
        "staffrequest/<int:staffid>/update/",
        StaffRequestUpdateView.as_view(),
        name="staff_request_update",
    ),
    path(
        "staffrequest/",
        StaffRequestListView.as_view(),
        name="staff_request_list",
    ),
    path(
        "staff_request/<int:pk>/",
        StaffRequestDetailView.as_view(),
        name="staff_request_detail",
    ),
]

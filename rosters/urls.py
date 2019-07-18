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
    PreferenceListView,
    PreferenceUpdateView,
    PreferenceDetailView,
    PreferenceDeleteView,
    PreferenceCreateView,
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
)

urlpatterns = [
    path("leave/<int:pk>/edit/", LeaveUpdateView.as_view(), name="leave_edit"),
    path("leave/<int:pk>/", LeaveDetailView.as_view(), name="leave_detail"),
    path(
        "leave/<int:pk>/delete/",
        LeaveDeleteView.as_view(),
        name="leave_delete",
    ),
    path("leave/new/", LeaveCreateView.as_view(), name="leave_new"),
    path("leave/", LeaveListView.as_view(), name="leave_list"),
    path("role/<int:pk>/edit/", RoleUpdateView.as_view(), name="role_edit"),
    path("role/<int:pk>/", RoleDetailView.as_view(), name="role_detail"),
    path(
        "role/<int:pk>/delete/", RoleDeleteView.as_view(), name="role_delete"
    ),
    path("role/new/", RoleCreateView.as_view(), name="role_new"),
    path("role/", RoleListView.as_view(), name="role_list"),
    path("shift/<int:pk>/edit/", ShiftUpdateView.as_view(), name="shift_edit"),
    path("shift/<int:pk>/", ShiftDetailView.as_view(), name="shift_detail"),
    path(
        "shift/<int:pk>/delete/",
        ShiftDeleteView.as_view(),
        name="shift_delete",
    ),
    path("shift/new/", ShiftCreateView.as_view(), name="shift_new"),
    path("shift/", ShiftListView.as_view(), name="shift_list"),
    path(
        "shiftrule/<int:pk>/edit/",
        ShiftRuleUpdateView.as_view(),
        name="shift_rule_edit",
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
        "shiftrule/new/", ShiftRuleCreateView.as_view(), name="shift_rule_new"
    ),
    path("shiftrule/", ShiftRuleListView.as_view(), name="shift_rule_list"),
    path(
        "shiftrulerole/<int:pk>/edit/",
        ShiftRuleRoleUpdateView.as_view(),
        name="shift_rule_role_edit",
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
        "shiftrulerole/<slug:shiftrule>/new/",
        ShiftRuleRoleCreateView.as_view(),
        name="shift_rule_role_new",
    ),
    path(
        "shiftrulerole/",
        ShiftRuleRoleListView.as_view(),
        name="shift_rule_role_list",
    ),
    path(
        "staffrule/<int:pk>/edit/",
        StaffRuleUpdateView.as_view(),
        name="staff_rule_edit",
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
        "staffrule/new/", StaffRuleCreateView.as_view(), name="staff_rule_new"
    ),
    path("staffrule/", StaffRuleListView.as_view(), name="staff_rule_list"),
    path(
        "staffruleshift/<int:pk>/edit/",
        StaffRuleShiftUpdateView.as_view(),
        name="staff_rule_shift_edit",
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
        "staffruleshift/<slug:staffrule>/new/",
        StaffRuleShiftCreateView.as_view(),
        name="staff_rule_shift_new",
    ),
    path(
        "staffruleshift/",
        StaffRuleShiftListView.as_view(),
        name="staff_rule_shift_list",
    ),
    path(
        "timeslot/<int:pk>/edit/",
        TimeSlotUpdateView.as_view(),
        name="timeslot_edit",
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
    path("timeslot/new/", TimeSlotCreateView.as_view(), name="timeslot_new"),
    path("timeslot/", TimeSlotListView.as_view(), name="timeslot_list"),
    path(
        "timeslot/generate",
        GenerateRosterView.as_view(),
        name="generate_roster",
    ),
    path(
        "timeslot/select",
        SelectRosterView.as_view(),
        name="select_roster",
    ),
    path("roster/", RosterListView.as_view(), name="roster_list"),
    path(
        "preference/<int:pk>/edit/",
        PreferenceUpdateView.as_view(),
        name="preference_edit",
    ),
    path(
        "preference/<int:pk>/",
        PreferenceDetailView.as_view(),
        name="preference_detail",
    ),
    path(
        "preference/<int:pk>/delete/",
        PreferenceDeleteView.as_view(),
        name="preference_delete",
    ),
    path(
        "preference/new/",
        PreferenceCreateView.as_view(),
        name="preference_new",
    ),
    path("preference/", PreferenceListView.as_view(), name="preference_list"),
    path("roster/download", download_csv, name="download_csv"),
    path("daygroup/", DayGroupListView.as_view(), name="day_group_list"),
    path(
        "daygroup/<int:pk>/edit/",
        DayGroupUpdateView.as_view(),
        name="day_group_edit",
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
        "daygroup/new/", DayGroupCreateView.as_view(), name="day_group_new"
    ),
    path("daygroupday/", DayGroupDayListView.as_view(), name="day_group_day_list"),
    path(
        "daygroupday/<int:pk>/edit/",
        DayGroupDayUpdateView.as_view(),
        name="day_group_day_edit",
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
        "daygroupday/<slug:daygroup>/new/", DayGroupDayCreateView.as_view(), name="day_group_day_new"
    ),
    path("daygroupday/", DayGroupDayListView.as_view(), name="day_group_day_list"),
    path("day/<int:pk>/edit/", DayUpdateView.as_view(), name="day_edit"),
    path("day/<int:pk>/", DayDetailView.as_view(), name="day_detail"),
    path(
        "day/<int:pk>/delete/", DayDeleteView.as_view(), name="day_delete"
    ),
    path("day/new/", DayCreateView.as_view(), name="day_new"),
    path("day/", DayListView.as_view(), name="day_list"),
]

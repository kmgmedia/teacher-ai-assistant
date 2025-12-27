# Multi-Teacher Support Guide

## Overview

The AI Teaching Assistant now supports multiple teachers working with the same system. Each teacher can view and manage only their assigned students.

## Features

### 1. **Teacher Column in Google Sheets**

- Added "Teacher" column (position 2, between Name and Age)
- 132 student records assigned to 3 teachers:
  - **Ms. Sarah Thompson**: 44 records (4 students × 11 subjects)
  - **Mr. James Wilson**: 44 records (4 students × 11 subjects)
  - **Mrs. Emily Davis**: 44 records (4 students × 11 subjects)

### 2. **Teacher Selector in Dashboard**

- Located in the sidebar at the top
- Dropdown showing "All Teachers" or select a specific teacher
- Selection persists across all pages in the session

### 3. **Filtered Views**

All pages respect the teacher filter:

#### **View Students Page**

- Shows only students assigned to the selected teacher
- Displays unique student count and total records for that teacher
- Grade filtering works within the teacher's students

#### **Report Generator**

- When loading from Google Sheets, shows only the selected teacher's students in dropdown
- Generated reports are contextualized to that teacher

#### **Parent Message**

- Auto-fills teacher name based on selection
- Messages are personalized with the teacher's name

## How to Use

1. **Select Your Teacher Profile**

   - Open the dashboard sidebar
   - Use the "Select Teacher" dropdown under "👨‍🏫 Select Teacher"
   - Choose your name or "All Teachers" (for admins)

2. **View Your Students**

   - Navigate to "👥 View Students"
   - You'll see only students assigned to you
   - Use grade filters to further narrow the view

3. **Generate Reports**

   - Go to "📊 Report Generator"
   - Check "Load student data from Google Sheets"
   - Select from your assigned students only

4. **Send Parent Messages**
   - Navigate to "💌 Parent Message"
   - Your teacher name is pre-filled
   - Draft messages for your students' parents

## Teacher Assignments

Current assignment strategy: **Round-robin by student name**

- Each student has the same teacher for all 11 subjects
- 12 students ÷ 3 teachers = 4 students per teacher

### Student-Teacher Mapping:

| Student Name   | Teacher            | Subjects Count |
| -------------- | ------------------ | -------------- |
| Emma Johnson   | Ms. Sarah Thompson | 11             |
| Liam Chen      | Mr. James Wilson   | 11             |
| Olivia Smith   | Mrs. Emily Davis   | 11             |
| Noah Williams  | Ms. Sarah Thompson | 11             |
| Ava Brown      | Mr. James Wilson   | 11             |
| Ethan Davis    | Mrs. Emily Davis   | 11             |
| Sophia Miller  | Ms. Sarah Thompson | 11             |
| Mason Wilson   | Mr. James Wilson   | 11             |
| Isabella Moore | Mrs. Emily Davis   | 11             |
| Lucas Taylor   | Ms. Sarah Thompson | 11             |
| Mia Anderson   | Mr. James Wilson   | 11             |
| Benjamin Lee   | Mrs. Emily Davis   | 11             |

## Adding New Teachers

To add more teachers or reassign students:

1. **Manual Assignment**:

   - Open the Google Sheet directly
   - Edit the "Teacher" column (Column B)
   - Assign teacher names to student rows

2. **Programmatic Assignment** (advanced):
   - Modify the teacher list in assignment scripts
   - Run batch update with new teacher assignments
   - Ensure all 132 rows have teacher values

## Technical Details

- **Data Structure**: Teacher column at index 1 (Column B)
- **Filter Logic**: `df[df['Teacher'] == selected_teacher]` applied before rendering
- **Session State**: Teacher selection stored in `st.session_state['selected_teacher']`
- **Cache**: 5-minute TTL on student data - refresh updates teacher filter
- **No Authentication**: Teacher selection is honor-system (trust-based)

## Future Enhancements

Potential improvements:

- ✅ Teacher authentication/login system
- ✅ Teacher-specific dashboards with analytics
- ✅ Bulk student reassignment tool
- ✅ Teacher collaboration features (notes, handoffs)
- ✅ Parent portal with teacher contact info

## Troubleshooting

**Q: I don't see the teacher selector**

- A: Ensure Google Sheets is configured in `.env`
- Check that `GOOGLE_SHEETS_CREDENTIALS` and `GOOGLE_SHEET_ID` are set

**Q: Teacher filter not working**

- A: Clear cache using "🔄 Refresh Data" button on View Students page
- Verify "Teacher" column exists in Google Sheet (Column B)

**Q: Some students missing**

- A: Check if they're assigned to another teacher
- Select "All Teachers" to see all students

**Q: Want to change teacher assignments**

- A: Edit Google Sheet directly (Column B) or run reassignment script
- Clear dashboard cache to see changes

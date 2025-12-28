from integrations.google_sheets import read_student_data
import pandas as pd

data = read_student_data()
print(f"Records: {len(data)}")
if data:
    df = pd.DataFrame(data)
    print(f"Columns: {df.columns.tolist()}")
    print(f"Has Teacher column? {'Teacher' in df.columns}")
    if 'Teacher' in df.columns:
        teachers = sorted(df['Teacher'].unique().tolist())
        print(f"Teachers found: {teachers}")
    print("\nFirst record:")
    print(data[0])

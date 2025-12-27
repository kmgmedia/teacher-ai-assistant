"""
Analytics functions for student performance analysis.
"""

import pandas as pd
from typing import Dict, List, Any


def calculate_class_statistics(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Calculate overall class statistics.
    
    Args:
        df: DataFrame with student data
        
    Returns:
        Dictionary with class statistics
    """
    if df.empty:
        return {}
    
    # Convert Score to numeric
    df = df.copy()
    df['Score'] = pd.to_numeric(df['Score'], errors='coerce')
    
    stats = {
        'total_students': df['Name'].nunique() if 'Name' in df.columns else 0,
        'total_records': len(df),
        'average_score': df['Score'].mean() if 'Score' in df.columns else 0,
        'median_score': df['Score'].median() if 'Score' in df.columns else 0,
        'highest_score': df['Score'].max() if 'Score' in df.columns else 0,
        'lowest_score': df['Score'].min() if 'Score' in df.columns else 0,
        'total_subjects': df['Subject'].nunique() if 'Subject' in df.columns else 0,
    }
    
    return stats


def get_subject_performance(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate average performance by subject.
    
    Args:
        df: DataFrame with student data
        
    Returns:
        DataFrame with subject averages
    """
    if df.empty or 'Subject' not in df.columns or 'Score' not in df.columns:
        return pd.DataFrame()
    
    # Convert Score to numeric
    df = df.copy()
    df['Score'] = pd.to_numeric(df['Score'], errors='coerce')
    
    subject_stats = df.groupby('Subject').agg({
        'Score': ['mean', 'median', 'min', 'max', 'count']
    }).round(1)
    
    subject_stats.columns = ['Average', 'Median', 'Min', 'Max', 'Students']
    subject_stats = subject_stats.reset_index()
    subject_stats = subject_stats.sort_values('Average', ascending=False)
    
    return subject_stats


def get_grade_performance(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate average performance by grade level.
    
    Args:
        df: DataFrame with student data
        
    Returns:
        DataFrame with grade averages
    """
    if df.empty or 'Grade' not in df.columns or 'Score' not in df.columns:
        return pd.DataFrame()
    
    # Convert Score to numeric
    df = df.copy()
    df['Score'] = pd.to_numeric(df['Score'], errors='coerce')
    
    grade_stats = df.groupby('Grade').agg({
        'Score': ['mean', 'median', 'count'],
        'Name': 'nunique'
    }).round(1)
    
    grade_stats.columns = ['Average Score', 'Median Score', 'Total Records', 'Unique Students']
    grade_stats = grade_stats.reset_index()
    grade_stats = grade_stats.sort_values('Grade')
    
    return grade_stats


def get_top_students(df: pd.DataFrame, n: int = 5) -> pd.DataFrame:
    """
    Get top performing students based on average score.
    
    Args:
        df: DataFrame with student data
        n: Number of top students to return
        
    Returns:
        DataFrame with top students
    """
    if df.empty or 'Name' not in df.columns or 'Score' not in df.columns:
        return pd.DataFrame()
    
    # Convert Score to numeric
    df = df.copy()
    df['Score'] = pd.to_numeric(df['Score'], errors='coerce')
    
    top_students = df.groupby('Name').agg({
        'Score': 'mean',
        'Grade': 'first',
        'Subject': 'count'
    }).round(1)
    
    top_students.columns = ['Average Score', 'Grade', 'Subjects Taken']
    top_students = top_students.reset_index()
    top_students = top_students.sort_values('Average Score', ascending=False).head(n)
    
    return top_students


def get_struggling_students(df: pd.DataFrame, threshold: float = 60, n: int = 5) -> pd.DataFrame:
    """
    Get students performing below threshold.
    
    Args:
        df: DataFrame with student data
        threshold: Score threshold for struggling students
        n: Maximum number of students to return
        
    Returns:
        DataFrame with struggling students
    """
    if df.empty or 'Name' not in df.columns or 'Score' not in df.columns:
        return pd.DataFrame()
    
    # Convert Score to numeric
    df = df.copy()
    df['Score'] = pd.to_numeric(df['Score'], errors='coerce')
    
    struggling = df.groupby('Name').agg({
        'Score': 'mean',
        'Grade': 'first',
        'Subject': 'count'
    }).round(1)
    
    struggling.columns = ['Average Score', 'Grade', 'Subjects']
    struggling = struggling.reset_index()
    struggling = struggling[struggling['Average Score'] < threshold]
    struggling = struggling.sort_values('Average Score').head(n)
    
    return struggling


def get_behavior_distribution(df: pd.DataFrame) -> Dict[str, int]:
    """
    Get distribution of behavior ratings.
    
    Args:
        df: DataFrame with student data
        
    Returns:
        Dictionary with behavior counts
    """
    if df.empty or 'Behavior' not in df.columns:
        return {}
    
    behavior_counts = df['Behavior'].value_counts().to_dict()
    return behavior_counts


def get_teacher_performance(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate performance statistics by teacher.
    
    Args:
        df: DataFrame with student data
        
    Returns:
        DataFrame with teacher statistics
    """
    if df.empty or 'Teacher' not in df.columns or 'Score' not in df.columns:
        return pd.DataFrame()
    
    # Convert Score to numeric
    df = df.copy()
    df['Score'] = pd.to_numeric(df['Score'], errors='coerce')
    
    teacher_stats = df.groupby('Teacher').agg({
        'Score': ['mean', 'median'],
        'Name': 'nunique',
        'Subject': 'count'
    }).round(1)
    
    teacher_stats.columns = ['Average Score', 'Median Score', 'Students', 'Total Records']
    teacher_stats = teacher_stats.reset_index()
    teacher_stats = teacher_stats.sort_values('Average Score', ascending=False)
    
    return teacher_stats

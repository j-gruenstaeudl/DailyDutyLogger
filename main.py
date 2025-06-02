import matplotlib.pyplot as plt
import datetime

def create_driver_logbook_line_diagram_ondemand(log_data):
    """
    Creates a driver's logbook diagram using line segments that only appear
    where an activity is defined, starting at the first entry's time.

    Args:
        log_data (dict): A dictionary containing logbook data for each day.
                         (Same structure as previous examples)
    """
    days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    num_days = len(days_of_week)

    fig, axes = plt.subplots(num_days, 1, figsize=(12, 2.5 * num_days), sharex=True)

    # Map activity types to numerical values for plotting
    activity_mapping = {
        'F': 0, # Driving
        'P': 1, # Break
        'A': 2  # Work
    }
    # Colors for different activity types
    colors = {
        'F': 'red',
        'P': 'yellow',
        'A': 'blue'
    }

    # Header information
    week_info = {
        'date_range': '24.02.2025 bis 28.02.2025',
        'monteur': 'Hans Mustermann',
        'week_number': 9
    }

    fig.suptitle(
        f"Wochenbericht vom {week_info['date_range']}   Monteur: {week_info['monteur']}   Woche: {week_info['week_number']}\n"
        f"Bitte um Einhaltung der gesetzlich vorgeschriebenen Mittagspause von 30 min nach 6 Arbeitsstunden!",
        fontsize=14, y=0.98
    )

    total_weekly_hours = 0

    for i, day in enumerate(days_of_week):
        ax = axes[i]
        daily_data = log_data.get(day, {'activities': [], 'total_hours': 0, 'km': 0})

        # Sort activities by start time to ensure correct plotting order and handling notes
        sorted_activities = sorted(daily_data['activities'], key=lambda x: x['start'])

        # Plot activities as individual line segments
        for activity in sorted_activities:
            start_time = activity['start']
            end_time = activity['end']
            activity_type = activity['type']
            note = activity.get('note', '')

            y_pos = activity_mapping[activity_type]

            # Plot the horizontal line segment for the activity duration
            ax.plot([start_time, end_time], [y_pos, y_pos],
                    color=colors.get(activity_type, 'gray'), linewidth=4, solid_capstyle='butt') # 'butt' for sharp ends

            # Add notes
            if note:
                ax.text(start_time + (end_time - start_time) / 2, y_pos + 0.3, note,
                        ha='center', va='bottom', fontsize=8, color='black')

        # Set up the Y-axis for activity types
        ax.set_yticks(list(activity_mapping.values()))
        ax.set_yticklabels(list(activity_mapping.keys()))
        ax.set_ylim(-0.5, len(activity_mapping) - 0.5) # Adjust y-limits to center labels

        # Set up the X-axis for hours
        ax.set_xticks(range(0, 25, 1)) # Hours from 0 to 24
        ax.set_xlim(0, 24)
        ax.tick_params(axis='x', length=4, labelbottom=True) # Show ticks and labels for x-axis

        ax.grid(axis='x', linestyle='--', alpha=0.7) # Grid lines for hours

        # Add day label on the left
        ax.text(-1.5, (len(activity_mapping) - 1) / 2, day, va='center', ha='right', fontsize=10, weight='bold', rotation=90)

        # Add daily summary (total hours and kilometers)
        ax.text(24.5, (len(activity_mapping) * 2 / 3) - 0.5, f"Std. {daily_data['total_hours']}", va='center', ha='left', fontsize=10)
        ax.text(24.5, (len(activity_mapping) * 1 / 3) - 0.5, f"km {daily_data['km']}", va='center', ha='left', fontsize=10)

        total_weekly_hours += daily_data['total_hours']

        # Remove spines
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['bottom'].set_visible(False)


    # Add weekly summary at the bottom
    fig.text(0.85, 0.02, f"Gesamt-Stunden: {total_weekly_hours}", ha='right', va='center', fontsize=12, weight='bold')

    plt.tight_layout(rect=[0, 0.05, 1, 0.95]) # Adjust layout to make space for suptitle and bottom text
    plt.show()

# Example Usage with some dummy data (same as before)
example_log_data = {
    'Monday': {
        'activities': [
            {'type': 'A', 'start': 0, 'end': 8, 'note': 'Preparation'},
            {'type': 'F', 'start': 8, 'end': 12, 'note': 'Route A'},
            {'type': 'P', 'start': 12, 'end': 13, 'note': 'Lunch break'},
            {'type': 'F', 'start': 13, 'end': 17, 'note': 'Route B'},
            {'type': 'A', 'start': 17, 'end': 18, 'note': 'Post-trip check'}
        ],
        'total_hours': 18,
        'km': 396
    },
    'Tuesday': {
        'activities': [
            {'type': 'A', 'start': 7, 'end': 8, 'note': 'Pre-trip check'},
            {'type': 'F', 'start': 8, 'end': 12, 'note': 'Delivery 1'},
            {'type': 'P', 'start': 12, 'end': 12.5, 'note': 'Short break'},
            {'type': 'F', 'start': 12.5, 'end': 16, 'note': 'Delivery 2'},
            {'type': 'A', 'start': 16, 'end': 17, 'note': 'Paperwork'}
        ],
        'total_hours': 10,
        'km': 361
    },
    'Wednesday': {
        'activities': [
            {'type': 'A', 'start': 6, 'end': 7.5, 'note': 'Loading'},
            {'type': 'F', 'start': 7.5, 'end': 12.5, 'note': 'Long haul'},
            {'type': 'P', 'start': 12.5, 'end': 13.5, 'note': 'Mandatory break'},
            {'type': 'F', 'start': 13.5, 'end': 16.5, 'note': 'Unloading'},
            {'type': 'A', 'start': 16.5, 'end': 17.5, 'note': 'Cleaning'}
        ],
        'total_hours': 11.5,
        'km': 250
    },
    'Thursday': {
        'activities': [
            {'type': 'A', 'start': 7, 'end': 8},
            {'type': 'F', 'start': 8, 'end': 12, 'note': 'City routes'},
            {'type': 'P', 'start': 12, 'end': 13},
            {'type': 'F', 'start': 13, 'end': 17, 'note': 'Suburban delivery'},
            {'type': 'A', 'start': 17, 'end': 18}
        ],
        'total_hours': 12,
        'km': 388
    },
    'Friday': {
        'activities': [
            {'type': 'A', 'start': 8, 'end': 9},
            {'type': 'F', 'start': 9, 'end': 12},
            {'type': 'P', 'start': 12, 'end': 12.5},
            {'type': 'F', 'start': 12.5, 'end': 15},
            {'type': 'A', 'start': 15, 'end': 16}
        ],
        'total_hours': 7,
        'km': 376
    },
    'Saturday': {
        'activities': [],
        'total_hours': 0,
        'km': 0
    },
    'Sunday': {
        'activities': [],
        'total_hours': 0,
        'km': 0
    }
}

create_driver_logbook_line_diagram_ondemand(example_log_data)
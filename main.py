import matplotlib.pyplot as plt
import datetime
import numpy as np # Import numpy for arange

def create_driver_logbook_step_diagram(log_data):
    """
    Creates a driver's logbook diagram using connected line segments (step plot)
    where lines start at the first entry's time and connect transitions.

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

        # Sort activities by start time to ensure correct plotting order
        sorted_activities = sorted(daily_data['activities'], key=lambda x: x['start'])

        # Plot activities and connect transitions
        for j, activity in enumerate(sorted_activities):
            start_time = activity['start']
            end_time = activity['end']
            activity_type = activity['type']
            note = activity.get('note', '')

            y_pos_current = activity_mapping[activity_type]

            # Plot the horizontal line segment for the activity duration
            ax.plot([start_time, end_time], [y_pos_current, y_pos_current],
                    color=colors.get(activity_type, 'gray'), linewidth=4, solid_capstyle='butt')

            # Add notes
            if note:
                ax.text(start_time + (end_time - start_time) / 2, y_pos_current + 0.3, note,
                        ha='center', va='bottom', fontsize=8, color='black')

            # Check for next activity to draw connecting vertical line
            if j < len(sorted_activities) - 1:
                next_activity = sorted_activities[j+1]
                next_start_time = next_activity['start']
                y_pos_next = activity_mapping[next_activity['type']]

                # If the next activity starts exactly where the current one ends
                if end_time == next_start_time:
                    # Draw a vertical line from current activity's end to next activity's start
                    # Use a neutral color like black for the connecting line
                    ax.plot([end_time, next_start_time], [y_pos_current, y_pos_next],
                            color='black', linewidth=1.5, linestyle='-')


        # Set up the Y-axis for activity types
        ax.set_yticks(list(activity_mapping.values()))
        ax.set_yticklabels(list(activity_mapping.keys()))
        ax.set_ylim(-0.5, len(activity_mapping) - 0.5) # Adjust y-limits to center labels

        # Set up the X-axis for hours with quarter-hour steps
        # This will set major ticks at every hour (0, 1, 2, ..., 24)
        ax.set_xticks(range(0, 25, 1))
        # This will add minor ticks every quarter hour
        ax.set_xticks(np.arange(0, 24.25, 0.25), minor=True) # Ensure it goes up to 24.0
        ax.set_xlim(0, 24)
        ax.tick_params(axis='x', length=4, labelbottom=True) # Show major ticks and labels for x-axis

        # Add grid lines for major ticks (full hours) and minor ticks (quarter hours)
        ax.grid(axis='x', which='major', linestyle='-', alpha=0.7) # Solid lines for hours
        ax.grid(axis='x', which='minor', linestyle=':', alpha=0.5) # Dotted lines for quarter hours


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
            {'type': 'F', 'start': 6, 'end': 8.5, 'note': 'Route A'},
            {'type': 'A', 'start': 8.5, 'end': 9.5, 'note': 'Work 1'},
            {'type': 'F', 'start': 9.5, 'end': 11.5, 'note': 'Route B'},
            {'type': 'P', 'start': 11.5, 'end': 12, 'note': 'brake'},
            {'type': 'A', 'start': 12, 'end': 14, 'note': 'Work 3'},
            {'type': 'F', 'start': 14, 'end':16.5, 'note': 'drive home'}
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

create_driver_logbook_step_diagram(example_log_data)
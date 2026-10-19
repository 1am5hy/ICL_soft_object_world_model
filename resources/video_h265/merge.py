import os

name_row1 = [
    "./push_reach_goal_agent0_eval_5.mp4",
    "./push_reach_goal_agent1_norl_eval_5.mp4",
    "./push_reach_goal_agent2_norl_eval_5.mp4",
    "./push_reach_goal_agent5_norl_eval_5.mp4",
    "./push_reach_goal_agent6_norl_eval_5.mp4",
    "./push_reach_goal_agent1_withrl_eval_5.mp4",
    "./push_reach_goal_agent2_withrl_eval_5.mp4",
    "./push_reach_goal_agent5_withrl_eval_5.mp4",
    "./push_reach_goal_agent6_withrl_eval_5.mp4",
]
name_row2 = [
    "./push_play_full_agent0_eval_5.mp4",
    "./push_play_full_agent1_norl_eval_5.mp4",
    "./push_play_full_agent2_norl_eval_5.mp4",
    "./push_play_full_agent5_norl_eval_5.mp4",
    "./push_play_full_agent6_norl_eval_5.mp4",
    "./push_play_full_agent1_withrl_eval_5.mp4",
    "./push_play_full_agent2_withrl_eval_5.mp4",
    "./push_play_full_agent5_withrl_eval_5.mp4",
    "./push_play_full_agent6_withrl_eval_5.mp4",
]
name_row3 = [
    "./push_play_stitch_agent0_eval_5.mp4",
    "./push_play_stitch_agent1_norl_eval_5.mp4",
    "./push_play_stitch_agent2_norl_eval_5.mp4",
    "./push_play_stitch_agent5_norl_eval_5.mp4",
    "./push_play_stitch_agent6_norl_eval_5.mp4",
    "./push_play_stitch_agent1_withrl_eval_5.mp4",
    "./push_play_stitch_agent2_withrl_eval_5.mp4",
    "./push_play_stitch_agent5_withrl_eval_5.mp4",
    "./push_play_stitch_agent6_withrl_eval_5.mp4",
]

def generate_ffmpeg_grid_command(row1, row2, row3, output="output.mp4"):
    all_rows = [row1, row2, row3]
    inputs = []
    filter_parts = []

    # Step 1: Define inputs
    for row in all_rows:
        for video in row:
            inputs.append(f"-i {video}")

    # Step 2: Build filter_complex
    input_index = 0
    row_labels = []
    for row_idx, row in enumerate(all_rows):
        labels = [f"[{i}:v]" for i in range(input_index, input_index + len(row))]
        row_label = f"[row{row_idx}]"
        row_labels.append(row_label)
        filter_parts.append(f"{''.join(labels)}hstack=inputs={len(row)}{row_label}")
        input_index += len(row)

    # Step 3: Stack rows vertically
    filter_parts.append(f"{''.join(row_labels)}vstack=inputs=3[outv]")

    # Step 4: Join everything together
    filter_complex = ";".join(filter_parts)
    full_command = f"ffmpeg {' '.join(inputs)} -filter_complex \"{filter_complex}\" -map \"[outv]\" {output}"

    return full_command


# Example usage
print(name_row1)
print(name_row2)
print(name_row3)
cmd = generate_ffmpeg_grid_command(name_row1, name_row2, name_row3, output="/tmp/grid.mp4")
print(cmd)


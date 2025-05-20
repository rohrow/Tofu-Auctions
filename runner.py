import subprocess

process1 = subprocess.Popen(["python3", "discord_bot.py"])
process2 = subprocess.Popen(["python3", "format_data.py"])

process1.wait()
process2.wait()
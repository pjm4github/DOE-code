import subprocess


class RunCommandLine:
    @staticmethod
    def runCommand(command):
        try:
            result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            # Print standard output
            if result.stdout:
                print(result.stdout.strip())

            # Print standard error
            if result.stderr:
                print(result.stderr.strip())

        except Exception as e:
            print("Exception @RunCommandLine:runCommand")
            print(str(e))
            raise e

# Example usage:
# command_to_run = "your_command_here"
# RunCommandLine.runCommand(command_to_run)

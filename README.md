# command_tools

## 示例

    import sys
    import time

    from command_tools.command import Command, RunCommand
    from command_tools.errors import DontHavePermissionError, CommandNotFindError


    @Command("time")
    def now_time(*_):
        return time.time()


    @Command("exit")
    def exit_(*_):
        sys.exit(0)


    run_command = RunCommand()


    def main():
        while True:
            cmd = input()
            try:
                ret = run_command.run_by_str(cmd, float("inf"))
                print(ret)
            except DontHavePermissionError as err:
                print(err, file=sys.stderr)
            except CommandNotFindError as err:
                print(err, file=sys.stderr)


    if __name__ == "__main__":
        main()

--------------------------------------------------
--------------------------------------------------
    
    !time
    1679916179.5732734
    #time
    1679916184.4938388
    $time
    1679916193.5063045
    /time
    1679916197.336521
    //time
    1679916199.5743005
    \time
    1679916202.4622855
    \\time
    1679916204.728234
    time
    Command Not Find! (Command: time)
    test
    Command Not Find! (Command: test)
    $exit

    进程已结束,退出代码0

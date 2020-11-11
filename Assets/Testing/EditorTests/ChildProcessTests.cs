using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Threading;
using NUnit.Framework;
using RL;

namespace Testing.EditorTests
{
    public class ChildProcessTests
    {
        static void Expect(string expected, Process p)
        {
            var actual = p.StandardOutput.ReadLine();
            Assert.AreEqual(expected, actual);
        }

        [Test]
        public void EchoCommandWorks()
        {
            using (var p = ProcessRunner.CreateProcess("tests/child_process/std_in_out_test.py")) {
                const string message = "Hello world";
                p.Start();
                p.StandardInput.WriteLine(message);
                Expect(message, p);
            }
        }

        [Test]
        public void PassingArgumentsWorks()
        {
            const string argument = "argument";
            const string filePath = "tests/child_process/arguments_test.py";
            var arguments = new Dictionary<string, string>();
            arguments.Add("test_parameter", argument);

            using (var p = ProcessRunner.CreateProcess(filePath, arguments)) {
                p.Start();
                Expect(ProcessRunner.BASE_SOURCES_DIR, p);
                Expect(argument, p);
            }
        }

        [Test]
        public void ImportsWork()
        {
            const string filePath = "tests/child_process/imports_test.py";

            using (var p = ProcessRunner.CreateProcess(filePath)) {
                p.Start();
                var line = p.StandardOutput.ReadLine();
                Console.WriteLine(line);
            }
        }

        [Test]
        public void InterruptsTest()
        {
            const string filePath = "tests/child_process/interrupts_test.py";

            using (var p = ProcessRunner.CreateProcess(filePath, separateWindow: true)) {
                p.Start();
                Thread.Sleep(1000);
                p.Kill();
                Thread.Sleep(1000);
            }
        }
    }
}

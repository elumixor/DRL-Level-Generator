using System;
using System.Threading;
using System.Threading.Tasks;
using Common.ByteConversions;
using NUnit.Framework;
using RemoteComputation;

namespace Testing.EditorTests
{
    public class CommunicationTest
    {
        object _lock = new object();
        object cond = new object();

        readonly SemaphoreSlim ss = new SemaphoreSlim(0, 1);

        Task T1()
        {
            return Task.Run(() => {
                Console.WriteLine("Start 1");
                Thread.Sleep(1000);
                ss.Release();
                Console.WriteLine("End 1");
            });
        }

        Task WaitsOnT1()
        {
            return Task.Run(() => {
                Console.WriteLine("Start 2");
                Thread.Sleep(500);
                Console.WriteLine("Sleep ended 2");

                Console.WriteLine("Before wait");
                ss.Wait();
                Console.WriteLine("After wait");

                Console.WriteLine("End 2");
            });
        }

        [Test]
        public void LockingTest()
        {
            Console.WriteLine("?");
            var t1 = T1();
            var t2 = WaitsOnT1();
            t1.Wait();
            t2.Wait();
            Console.WriteLine("Finished");
        }

        [Test]
        public void TestCommunication()
        {
            var task = Communicator.Send(Message.Test(5.ToBytes()));
            task.Wait();
            Console.WriteLine(task.Result);
        }
    }
}

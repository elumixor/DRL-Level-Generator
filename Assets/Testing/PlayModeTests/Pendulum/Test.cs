using System.Collections;
using NUnit.Framework;
using UnityEngine;
using UnityEngine.SceneManagement;
using UnityEngine.TestTools;

namespace Testing.PlayModeTests.Pendulum {
    public class Test {
        // A UnityTest behaves like a coroutine in PlayMode
        // and allows you to yield null to skip a frame in EditMode
        [UnityTest]
        public IEnumerator TestWithEnumeratorPasses() {
            SceneManager.LoadScene("Pendulum");
            yield return null;
            yield return new WaitForSeconds(5f);
        }
    }
}
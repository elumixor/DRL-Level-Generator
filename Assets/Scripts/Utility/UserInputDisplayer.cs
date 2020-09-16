using System.Collections;
using TMPro;
using UnityEngine;

namespace Utility {
    [RequireComponent(typeof(TextMeshProUGUI))]
    public class UserInputDisplayer : MonoBehaviour {
        [SerializeField] private float fadeTime;

        private string Text {
            set {
                var tmpro = GetComponent<TextMeshProUGUI>();
                tmpro.text = value;
                if (currentCoroutine != null) StopCoroutine(currentCoroutine);

                IEnumerator FadeCoroutine() {
                    var elapsed = 0f;
                    while (elapsed < fadeTime) {
                        elapsed += Time.deltaTime;
                        yield return null;
                    }

                    tmpro.text = "";
                }

                currentCoroutine = FadeCoroutine();
                StartCoroutine(currentCoroutine);
            }
        }

        private IEnumerator currentCoroutine;


        void Update() {
            HandleInput();
        }

        private void HandleInput() {
            if (Input.GetMouseButtonDown(0)) {
                Text = "Click";
                return;
            }
        }
    }
}
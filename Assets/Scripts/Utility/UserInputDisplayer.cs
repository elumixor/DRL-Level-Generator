﻿using System.Collections;
using TMPro;
using UnityEngine;

namespace Utility {
    [RequireComponent(typeof(TextMeshProUGUI))]
    public class UserInputDisplayer : MonoBehaviour {
        [SerializeField] float fadeTime;

        string Text {
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

        IEnumerator currentCoroutine;


        void Update() { HandleInput(); }

        void HandleInput() {
            if (Input.GetMouseButtonDown(0)) {
                Text = "Click";
                return;
            }
        }
    }
}
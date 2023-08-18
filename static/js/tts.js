'speechSynthesis' in window ? console.log("Web Speech API supported!") : console.log("Web Speech API not supported :-(")

const synth = window.speechSynthesis

function startVoiceKor(text) {
  console.log(text)
  const utterThis = new SpeechSynthesisUtterance(text)
  utterThis.lang = "ko-KR"
  synth.speak(utterThis)
}

function startVoiceEng(text) {
  console.log(text)
  const utterThis = new SpeechSynthesisUtterance(text)
  utterThis.lang = "en-US"
  synth.speak(utterThis)
}
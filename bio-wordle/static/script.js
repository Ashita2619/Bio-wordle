let targetWord = "";
let attempts = 0;
const maxAttempts = 4;

console.log("Script loaded");

document.addEventListener("DOMContentLoaded", () => {
  fetch("/get-word")
    .then(response => response.json())
    .then(data => {
      targetWord = data.word.toLowerCase().replace(/\s+/g, '');
      console.log("Target word:", targetWord);

      const input = document.getElementById("guess-input");
      input.setAttribute("maxlength", targetWord.length);

      createEmptyBoard(targetWord.length);

      // Submit guess on Enter key press
      document.getElementById("guess-input").addEventListener("keydown", function(e) {
        if (e.key === "Enter") {
          submitGuess();
        }
      });
    });
});



function createEmptyBoard(wordLength) {
  const board = document.getElementById("game-board");
  board.innerHTML = "";

  for (let r = 0; r < maxAttempts; r++) {
    const row = document.createElement("div");
    row.classList.add("guess-row");
    row.id = `row-${r + 1}`;

    for (let c = 0; c < wordLength; c++) {
      const box = document.createElement("div");
      box.classList.add("letter-box");
      row.appendChild(box);
    }

    board.appendChild(row);
    console.log(`Creating row ${r + 1}`);
  }
}



function submitGuess() {
  if (attempts >= maxAttempts) {
    document.getElementById("message").textContent = "No more guesses! Try again tomorrow.";
    return;
  }

  const input = document.getElementById("guess-input");
  const guess = input.value.toLowerCase().trim();
  input.value = "";

  if (!guess || guess.length !== targetWord.length) {
    document.getElementById("message").textContent = `Enter a ${targetWord.length}-letter word.`;
    return;
  }

  const row = document.getElementById(`row-${attempts + 1}`);
  const boxes = row.getElementsByClassName("letter-box");

  // Animate each letter with a delay
  for (let i = 0; i < targetWord.length; i++) {
    setTimeout(() => {
      boxes[i].textContent = guess[i];
      boxes[i].classList.remove("correct", "present", "absent");
      boxes[i].classList.add("flip"); // start flip

      // After flip, set color
      setTimeout(() => {
        boxes[i].classList.remove("flip");
        if (guess[i] === targetWord[i]) {
          boxes[i].classList.add("correct");
        } else if (targetWord.includes(guess[i])) {
          boxes[i].classList.add("present");
        } else {
          boxes[i].classList.add("absent");
        }
      }, 150); // half the flip duration
    }, i * 200); // delay between letters
  }

  attempts++;

  // Show message after last letter animation completes
  setTimeout(() => {
    if (guess === targetWord) {
      document.getElementById("message").textContent = "🎉 You guessed it!";
    } else if (attempts >= maxAttempts) {
      document.getElementById("message").textContent = `Out of guesses! The word was "${targetWord}".`;
    } else {
      document.getElementById("message").textContent = `Try again! (${maxAttempts - attempts} left)`;
    }
  }, targetWord.length * 200 + 150);
}
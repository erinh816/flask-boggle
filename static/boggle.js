"use strict";

const $playedWords = $("#words");
const $form = $("#newWordForm");
const $wordInput = $("#wordInput");
const $message = $(".msg");
const $table = $("table");

const GAME_ID_KEY = "gameId";
const WORD_KEY = "word";

let gameId;


/** Start */

async function start() {
  const response = await fetch(`/api/new-game`, {
    method: "POST",
  });
  const gameData = await response.json();

  gameId = gameData.gameId;
  let board = gameData.board;

  displayBoard(board);
}

/** Display board */

function displayBoard(board) {
  // $table.empty();
  // loop over board and create the DOM tr/td structure
  $table.empty();
  for (let i = 0; i < board.length; i++) {
    const $row = $(`<tr>`);
    for (let j = 0; j < board[0].length; j++) {
      const letterMarkdown = `<td data-row-id=${i} data-column-id=${j}>`;
      const $letterElement = $(letterMarkdown);
      $letterElement.text(board[i][j]);
      $row.append($letterElement);
    }
    $table.append($row);
  }
}

async function handleWordSubmit(evt) {
  evt.preventDefault();
  const word = $('#wordInput').val();
  const options = {
    GAME_ID_KEY: gameId,
    WORD_KEY: word
  };

  const response = await fetch(`/api/score-word`, {
    method: "POST",
    body: JSON.stringify(options),
    headers: {
      "Content-Type": "application/json"
    }
  });
  const responseData = await response.json();
  const result = responseData['result'];

  let resultMessage = "";
  if (result !== "not-word" || result === "not-on-board") {
    resultMessage = "Try again!";
    $message.text(resultMessage)
  } else if (result == "ok") {
    const $word = $('<li>').text(word);
    $playedWords.append($word)
  }


}

$form.on("submit", handleWordSubmit);

start();
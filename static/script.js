document.getElementById('startGame').addEventListener('click', () => {
    fetch('/start')
        .then(response => response.json())
        .then(data => {
            document.getElementById('gameStatus').textContent = data.message;
        });
});

document.getElementById('submitGuess').addEventListener('click', () => {
    const guess = document.getElementById('userGuess').value;
    fetch('/guess', { // Note: Update this to the correct route if you change it in your Flask app
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ number: parseInt(guess, 10) }),
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('guessResult').textContent = data.message;
        if (!data.message.includes('Too')) {
            document.getElementById('gameStatus').textContent = 'Game over. Start a new game.';
        }
    });
});

var roundLogEl = document.querySelector('.accuracy');

anime({
  targets: roundLogEl,
  innerHTML: [0, 100],
  easing: 'linear',
  round: 10 // Will round the animated value to 1 decimal
});

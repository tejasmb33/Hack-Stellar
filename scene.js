// Reading pages retain their existing quiet background. The new renderer is home-only.
if (document.body.classList.contains('directory')) {
  import('./visuals/quiet-scene.js');
} else {
  import('./visuals/experience.js').then(({startExperience}) => startExperience()).catch(error => {
    console.error('Cosmos could not start:', error);
    document.body.classList.add('scene-unavailable');
  });
}

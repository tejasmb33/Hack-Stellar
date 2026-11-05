// The directory reuses the finalized home renderer. Full briefs keep their quiet background.
if (document.body.classList.contains('directory') && !document.body.classList.contains('cosmic-directory')) {
  import('./visuals/quiet-scene.js');
} else {
  import('./visuals/experience.js').then(({startExperience}) => startExperience()).catch(error => {
    console.error('Cosmos could not start:', error);
    document.body.classList.add('scene-unavailable');
  });
}

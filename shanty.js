/* Rolled-scroll intro + sampled Wellerman.
 *
 * Browsers refuse to start audio without a user gesture, so the page opens as a
 * rolled-up chart: the tap that unfurls it is the same gesture that unlocks
 * sound. The melody is the traditional shanty (public domain), played through
 * WebAudioFont sampled instruments (accordion lead, steel guitar bass).
 */
(function () {
  'use strict';

  /* ---- music ---- */
  var ctx = null, player = null, out = null, loopTimer = null, playing = false;
  var LEAD = window._tone_0210_Aspirin_sf2_file;
  var BASSFONT = window._tone_0250_Aspirin_sf2_file;

  var EIGHTH = 0.21; /* ~143bpm eighths — a brisk rowing pace */

  /* [midi, eighths]; 0 = rest. D minor. */
  var A2 = 45, C3 = 48, D3 = 50, F3 = 53, G3 = 55;
  var A3 = 57, C4 = 60, D4 = 62, E4 = 64, F4 = 65, G4 = 67, A4 = 69, C5 = 72;
  var MELODY = [
    /* There once was a ship that put to sea */
    [A3, 1], [D4, 1], [D4, 1], [D4, 1], [D4, 1], [F4, 1], [E4, 1], [D4, 2],
    /* and the name of the ship was the Billy of Tea */
    [E4, 1], [E4, 1], [E4, 1], [E4, 1], [E4, 1], [A3, 1], [C4, 1], [C4, 1], [A3, 2],
    /* the winds blew up, her bow dipped down */
    [A3, 1], [D4, 1], [D4, 1], [D4, 1], [D4, 1], [F4, 1], [A4, 1], [A4, 2],
    /* oh blow, my bully boys, blow */
    [G4, 1], [G4, 1], [E4, 1], [C4, 1], [D4, 3], [0, 1],
    /* Soon may the Wellerman come */
    [F4, 1], [F4, 1], [A4, 1], [A4, 1], [A4, 1], [A4, 2],
    /* to bring us sugar and tea and rum */
    [G4, 1], [G4, 1], [G4, 1], [G4, 1], [E4, 1], [C4, 1], [C4, 2],
    /* one day when the tonguing is done */
    [D4, 1], [F4, 1], [F4, 1], [F4, 1], [F4, 1], [A4, 1], [C5, 2],
    /* we'll take our leave and go */
    [A4, 1], [G4, 1], [E4, 1], [C4, 1], [D4, 4],
  ];
  /* Bass roots, one per 4 eighths; padded/looped to the melody length. */
  var BASS = [D3, A2, D3, A2, C3, A2, C3, D3, D3, A2, D3, F3, C3, C3, D3, D3,
              F3, F3, C3, C3, D3, D3, F3, G3, C3, C3, D3, D3];

  function scheduleLoop(t0) {
    var t = t0, total = 0, i;
    for (i = 0; i < MELODY.length; i++) {
      var m = MELODY[i][0], beats = MELODY[i][1], dur = beats * EIGHTH;
      if (m) player.queueWaveTable(ctx, out, LEAD, t, m, dur * 0.95, 0.5);
      t += dur;
      total += beats;
    }
    var slots = Math.ceil(total / 4);
    for (i = 0; i < slots; i++) {
      var b = BASS[i % BASS.length];
      player.queueWaveTable(ctx, out, BASSFONT, t0 + i * 4 * EIGHTH, b, 4 * EIGHTH * 0.95, 0.35);
    }
    var loopDur = total * EIGHTH;
    loopTimer = setTimeout(function () {
      if (playing) scheduleLoop(t0 + loopDur);
    }, (loopDur - 0.25) * 1000);
  }

  function startMusic() {
    if (playing) return;
    if (!window.WebAudioFontPlayer || !LEAD || !BASSFONT) return;
    if (!ctx) {
      var AC = window.AudioContext || window.webkitAudioContext;
      if (!AC) return;
      ctx = new AC();
      player = new WebAudioFontPlayer();
      player.adjustPreset(ctx, LEAD);
      player.adjustPreset(ctx, BASSFONT);
      var reverb = player.createReverberator(ctx);
      reverb.output.connect(ctx.destination);
      out = reverb.input;
    }
    if (ctx.state === 'suspended') ctx.resume();
    playing = true;
    /* adjustPreset decodes sample zones asynchronously; scheduling before
       every zone has a buffer plays silence. loader.waitLoad can't be used
       here — it only tracks fonts the loader itself fetched. */
    (function whenDecoded() {
      if (player.loader.loaded('_tone_0210_Aspirin_sf2_file') &&
          player.loader.loaded('_tone_0250_Aspirin_sf2_file')) {
        if (playing) scheduleLoop(ctx.currentTime + 0.08);
      } else {
        setTimeout(whenDecoded, 100);
      }
    })();
  }

  /* ---- rolled-scroll intro ---- */
  function makeOverlay() {
    var ov = document.createElement('div');
    ov.id = 'furl';
    ov.innerHTML =
      '<div class="furl-half furl-top"><div class="furl-paper"></div><div class="furl-rod"></div></div>' +
      '<div class="furl-half furl-bottom"><div class="furl-rod"></div><div class="furl-paper"></div></div>' +
      '<div class="furl-label">Tap to unfurl yer chart</div>';
    document.body.appendChild(ov);
    document.body.classList.add('furled');
    ov.addEventListener('pointerdown', function () {
      startMusic();
      ov.classList.add('open');
      document.body.classList.remove('furled');
      setTimeout(function () {
        if (ov.parentNode) ov.parentNode.removeChild(ov);
      }, 1100);
    }, { once: true });
  }

  function init() {
    makeOverlay();
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();

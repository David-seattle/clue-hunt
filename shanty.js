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

  var EIGHTH = 0.25; /* 120bpm quarters — a steady rowing pace */

  /* [midi, eighths]; 0 = rest. The Wellerman in E minor, transcribed from the
   * ABC setting at thesession.org/tunes/20383 (setting 2): 2/4, L=1/8. */
  var E4 = 64, Fs4 = 66, G4 = 67, A4 = 69, B4 = 71, C5 = 72, D5 = 74, E5 = 76;
  var MELODY = [
    /* pickup */
    [B4, 2],
    /* There once was a ship that put to sea */
    [E4, 2], [E4, 1], [E4, 1], [E4, 2], [G4, 1], [G4, 1],
    [B4, 2], [B4, 2], [B4, 2], [B4, 1], [B4, 1],
    /* the name of the ship was the Billy of Tea */
    [C5, 2], [A4, 1], [A4, 1], [A4, 2], [C5, 1], [C5, 1],
    [E5, 1], [E5, 1], [B4, 2], [B4, 2],
    /* the winds blew up, her bow dipped down */
    [B4, 2],
    [E4, 2], [Fs4, 1], [Fs4, 1], [G4, 2], [A4, 1], [A4, 1],
    [B4, 2], [B4, 2], [B4, 2], [B4, 1], [B4, 1],
    /* oh blow, my bully boys, blow */
    [C5, 2], [A4, 2], [G4, 1], [G4, 1], [Fs4, 2],
    [E4, 6], [0, 2],
    /* Soon may the Wellerman come */
    [E5, 4], [E5, 3], [C5, 1],
    /* to bring us sugar and tea and rum */
    [D5, 1], [D5, 1], [G4, 2], [G4, 3], [G4, 1],
    /* one day when the tonguing is done */
    [C5, 2], [A4, 2], [A4, 1], [B4, 1], [C5, 2],
    /* we'll take our leave and go */
    [B4, 2], [G4, 2], [E4, 4],
    /* chorus, second half */
    [E5, 4], [E5, 2], [D5, 1], [C5, 1],
    [D5, 1], [D5, 1], [G4, 2], [G4, 2], [G4, 2],
    [B4, 2], [A4, 2], [G4, 2], [Fs4, 2],
    [E4, 5], [0, 1],
  ];
  /* The chorus begins this many eighths in; from there a quieter second
     accordion joins a diatonic third below, like the crew coming in. */
  var CHORUS_AT = 66;
  var THIRD_BELOW = {76: 72, 74: 71, 72: 69, 71: 67, 69: 66, 67: 64, 66: 62, 64: 60};

  /* Chord roots, one per 4 eighths, following Em / Am / B / C / G harmony. */
  var E2 = 40, G2 = 43, A2 = 45, B2 = 47, C3 = 48;
  var BASS = [E2, E2, E2, B2, A2, A2, E2, B2,
              E2, E2, B2, B2, A2, B2, E2, E2,
              C3, C3, G2, G2, A2, A2, E2, E2,
              C3, C3, G2, G2, B2, B2, E2, E2];

  function scheduleLoop(t0) {
    var t = t0, total = 0, i;
    for (i = 0; i < MELODY.length; i++) {
      var m = MELODY[i][0], beats = MELODY[i][1], dur = beats * EIGHTH;
      if (m) {
        player.queueWaveTable(ctx, out, LEAD, t, m, dur * 0.95, 0.5);
        if (total >= CHORUS_AT && THIRD_BELOW[m]) {
          player.queueWaveTable(ctx, out, LEAD, t, THIRD_BELOW[m], dur * 0.95, 0.22);
        }
      }
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

  /* Ship's bell for correct gate answers: two bright strikes of a
     three-partial sine cluster. Exposed for the gate pages' inline script. */
  window.shantyBell = function () {
    var AC = window.AudioContext || window.webkitAudioContext;
    if (!AC) return;
    if (!ctx) ctx = new AC();
    if (ctx.state === 'suspended') ctx.resume();
    var dest = out || ctx.destination;
    function strike(t0) {
      var partials = [[830, 1.0], [1245, 0.55], [2075, 0.28]];
      for (var i = 0; i < partials.length; i++) {
        var osc = ctx.createOscillator();
        var g = ctx.createGain();
        osc.frequency.value = partials[i][0];
        g.gain.setValueAtTime(partials[i][1], t0);
        g.gain.exponentialRampToValueAtTime(0.0001, t0 + 1.1);
        osc.connect(g);
        g.connect(dest);
        osc.start(t0);
        osc.stop(t0 + 1.2);
      }
    }
    strike(ctx.currentTime + 0.02);
    strike(ctx.currentTime + 0.3);
  };

  /* ---- rolled-scroll intro ---- */
  function makeOverlay() {
    var ov = document.createElement('div');
    ov.id = 'furl';
    ov.innerHTML = '<div class="furl-label">Tap to unfurl yer chart</div>';
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

import { useEffect, useState } from "react";
import { Piano, KeyboardShortcuts, MidiNumbers } from "react-piano";
import "react-piano/dist/styles.css";
import * as Tone from "tone";

type Props = {
  audioUrl: string;
};

export default function SamplePiano({ audioUrl }: Props) {
  const [buffer, setBuffer] = useState<Tone.ToneAudioBuffer | null>(null);

  const firstNote = MidiNumbers.fromNote("C4");
  const lastNote = MidiNumbers.fromNote("C5");
  const keyboardShortcuts = KeyboardShortcuts.create({
    firstNote,
    lastNote,
    keyboardConfig: KeyboardShortcuts.HOME_ROW,
  });

  useEffect(() => {
    if (audioUrl) {
      const loadBuffer = async () => {
        const newBuffer = await new Tone.ToneAudioBuffer(audioUrl);
        setBuffer(newBuffer);
      };
      loadBuffer();
    }
  }, [audioUrl]);

  const playNote = (midiNumber: number) => {
    if (!buffer) return;

    const gain = new Tone.Gain(0.2).toDestination(); // Adjust volume here

    const player = new Tone.Player({
      url: buffer,
      fadeIn: 0.01,
      fadeOut: 0.01,
    }).connect(gain);

    const baseMidi = 60; // Middle C
    const semitoneShift = midiNumber - baseMidi;
    player.playbackRate = Math.pow(2, semitoneShift / 12);
    player.start();
  };

  return (
    <div className="mt-8">
      <Piano
        noteRange={{ first: firstNote, last: lastNote }}
        playNote={playNote}
        stopNote={() => {}}
        keyboardShortcuts={keyboardShortcuts}
        width={600}
      />
    </div>
  );
}

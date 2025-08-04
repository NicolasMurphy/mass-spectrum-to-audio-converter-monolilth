import { type NameAndAccessionProps } from "../types";

export default function NameAndAccession({
  compoundName,
  accession,
}: NameAndAccessionProps) {
  const accessionUrl = `https://massbank.eu/MassBank/RecordDisplay?id=${accession}`;

  return (
    <div className="text-center mb-4 space-y-1">
      <p>
        <span className="font-semibold">Compound:</span> {compoundName}
      </p>
      <p>
        <span className="font-semibold">Accession:</span>{" "}
        <a
          href={accessionUrl}
          className="link text-info"
          target="_blank"
          rel="noopener noreferrer"
        >
          {accession}
        </a>
      </p>
    </div>
  );
}

import { type StatusMessageProps } from "../types";

export default function StatusMessage({ status }: StatusMessageProps) {
  if (!status) return null;

  return (
    <div className="text-sm text-center mb-4">
      {status === "Fetching audio..." ? (
        <span className="loading loading-spinner text-primary"></span>
      ) : (
        <span>{status}</span>
      )}
    </div>
  );
}

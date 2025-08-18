export default function EmptyDataPlaceholder() {
  return (
    <>
      <div className="text-center py-8 text-gray-500">
        <div className="text-lg mb-2">No spectrum data yet</div>
        <div className="text-sm">
          Enter a compound name to generate audio and see the data
          transformation
        </div>
      </div>
    </>
  );
}

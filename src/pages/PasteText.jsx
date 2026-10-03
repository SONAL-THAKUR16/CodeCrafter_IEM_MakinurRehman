import { useState } from "react";

function PasteText() {
  const [text, setText] = useState("");
  const [result, setResult] = useState("");

  function analyzeText() {
    if (!text.trim()) {
      setResult("Please enter some feedback first.");
      return;
    }

    const lowerText = text.toLowerCase();

    if (
      lowerText.includes("stress") ||
      lowerText.includes("tired") ||
      lowerText.includes("pressure")
    ) {
      setResult("Possible stress detected in the feedback.");
    } else if (
      lowerText.includes("confused") ||
      lowerText.includes("difficult")
    ) {
      setResult("Possible academic difficulty detected.");
    } else {
      setResult("No major negative emotion detected.");
    }
  }

  return (
    <div>
      <h1 className="text-3xl font-bold text-slate-800">
        Paste Student Feedback
      </h1>

      <p className="text-slate-500 mt-1 mb-6">
        Enter feedback to perform basic emotion analysis.
      </p>

      <div className="bg-white border rounded-xl p-6">
        <textarea
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Example: I am feeling stressed because of too many assignments..."
          className="w-full h-48 border rounded-lg p-4 outline-none focus:ring-2 focus:ring-blue-500"
        />

        <button
          onClick={analyzeText}
          className="mt-4 px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
        >
          Analyze Feedback
        </button>

        {result && (
          <div className="mt-5 p-4 bg-slate-100 rounded-lg">
            <strong>Analysis:</strong>
            <p className="mt-1">{result}</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default PasteText;
import { Upload } from "lucide-react";

function UploadFeedback() {
  return (
    <div>
      <h1 className="text-3xl font-bold text-slate-800">
        Upload Feedback
      </h1>

      <p className="text-slate-500 mt-1 mb-6">
        Upload student feedback data for analysis.
      </p>

      <div className="bg-white border rounded-xl p-10 text-center">
        <Upload
          size={50}
          className="mx-auto text-blue-500 mb-4"
        />

        <h2 className="text-xl font-semibold">
          Upload a CSV file
        </h2>

        <p className="text-slate-500 mt-2 mb-5">
          Select your student feedback dataset.
        </p>

        <input
          type="file"
          accept=".csv"
          className="mx-auto block"
        />
      </div>
    </div>
  );
}

export default UploadFeedback;
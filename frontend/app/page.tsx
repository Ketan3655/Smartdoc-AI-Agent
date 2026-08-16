"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import {
  getDocuments,
  uploadDocument,
  deleteDocument,
} from "../src/lib/api";
import ChatWindow from "../src/components/ChatWindow";
type Document = {
  id: string;
  filename: string;
  file_type: string;
  created_at: string;
};

export default function Home() {

  const router = useRouter();

  const [authChecking, setAuthChecking] = useState(true);

  const [documents, setDocuments] = useState<Document[]>([]);
  const [loading, setLoading] = useState(true);
  const [uploading, setUploading] = useState(false);

  const [uploadStatus, setUploadStatus] = useState("");
  const [selectedDocument, setSelectedDocument] =
    useState<string | null>(null);


  useEffect(() => {
    const token = localStorage.getItem("access_token");

    if (!token) {
      router.replace("/login");
      return;
    }

    setAuthChecking(false);
  }, [router]);



  function handleLogout() {
    localStorage.removeItem("access_token");
    router.replace("/login");
  }

  async function loadDocuments() {
    try {
      const data = await getDocuments();

      setDocuments(data.documents || []);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadDocuments();
  }, []);

  async function handleUpload(
    event: React.ChangeEvent<HTMLInputElement>
  ) {
    const file = event.target.files?.[0];

    if (!file) return;

    try {
      setUploading(true);
      setUploadStatus("Uploading document...");

      await uploadDocument(file);

      setUploadStatus("Document processed successfully.");

      await loadDocuments();

      setTimeout(() => {
        setUploadStatus("");
      }, 3000);
    } catch (error) {
      console.error(error);
      setUploadStatus("Failed to process document.");
    } finally {
      setUploading(false);
      event.target.value = "";
    }
  }

  async function handleDelete(
    documentId: string
  ) {
    try {
      await deleteDocument(documentId);

      if (selectedDocument === documentId) {
        setSelectedDocument(null);
      }

      await loadDocuments();
    } catch (error) {
      console.error(error);
      alert("Delete failed");
    }
  }
  if (authChecking) {
    return (
      <main className="flex min-h-screen items-center justify-center bg-slate-950 text-white">
        <p className="text-slate-400">
          Checking authentication...
        </p>
      </main>
    );
  }
  return (
    <main className="flex h-screen bg-slate-950 text-white">

      {/* Sidebar */}
      <aside className="w-80 border-r border-slate-800 bg-slate-900 p-5">

        <div className="mb-8">
          <h1 className="text-2xl font-bold">
            SmartDoc AI
          </h1>

          <p className="mt-1 text-sm text-slate-400">
            Chat with your documents
          </p>
        </div>
        <button
          onClick={handleLogout}
          className="mt-6 w-full rounded-xl bg-blue-600 border border-slate-700 px-4 py-3 text-sm font-medium text-slate-300 transition hover:bg-slate-800 hover:text-white"
        >
          Logout
        </button>

        {/* Upload */}
        <label className="mb-6 block cursor-pointer">
          <div className="rounded-xl bg-blue-600 px-4 py-3 text-center font-medium transition hover:bg-blue-500">
            {uploading ? "Processing..." : "+ Upload Document"}
          </div>

          <input
            type="file"
            accept=".pdf,.docx,.txt"
            className="hidden"
            onChange={handleUpload}
            disabled={uploading}
          />
        </label>
        {uploadStatus && (
          <p className="mb-5 text-center text-sm text-slate-400">
            {uploadStatus}
          </p>
        )}
        <div>
          <h2 className="mb-3 text-xs font-semibold uppercase tracking-wider text-slate-500">
            Documents
          </h2>

          {loading ? (
            <p className="text-sm text-slate-500">
              Loading documents...
            </p>
          ) : documents.length === 0 ? (
            <p className="text-sm text-slate-500">
              No documents uploaded
            </p>
          ) : (
            <div className="space-y-2">

              {documents.map((document) => (

                <div
                  key={document.id}
                  className={`group flex items-center justify-between rounded-lg p-3 transition ${selectedDocument === document.id
                    ? "bg-blue-600/20 border border-blue-500/40"
                    : "hover:bg-slate-800"
                    }`}
                >

                  <button
                    onClick={() =>
                      setSelectedDocument(document.id)
                    }
                    className="flex min-w-0 flex-1 items-center gap-3 text-left"
                  >

                    <span className="text-lg">
                      📄
                    </span>

                    <span className="truncate text-sm">
                      {document.filename}
                    </span>

                  </button>

                  <button
                    onClick={() =>
                      handleDelete(document.id)
                    }
                    className="ml-2 hidden text-slate-500 hover:text-red-400 group-hover:block"
                  >
                    ×
                  </button>

                </div>

              ))}

            </div>
          )}
        </div>

      </aside>

      {/* Main area */}
      <section className="flex flex-1 flex-col">

        <header className="border-b border-slate-800 px-8 py-5">
          <h2 className="text-lg font-semibold">
            {selectedDocument
              ? "Document Chat"
              : "Welcome to SmartDoc AI"}
          </h2>

          <p className="text-sm text-slate-400">
            {selectedDocument
              ? "Ask questions about your selected document."
              : "Upload a document to start chatting."}
          </p>
        </header>

        <div className="flex flex-1 items-center justify-center">

          {!selectedDocument ? (
            <div className="text-center">

              <div className="mb-4 text-6xl">
                📚
              </div>

              <h2 className="text-2xl font-semibold">
                Chat with your documents
              </h2>

              <p className="mt-2 text-slate-400">
                Upload a PDF, DOCX, or TXT file
                to get started.
              </p>

            </div>
          ) : (
            <ChatWindow documentId={selectedDocument} />
          )}

        </div>

      </section>
      <footer className="mt-auto border-t border-gray-200 py-4 text-center text-sm text-gray-500 dark:border-gray-800 dark:text-gray-400">
  Developed by <span className="font-medium text-gray-700 dark:text-gray-200">Ketan Prajapati</span>
</footer>

    </main>
  );
}


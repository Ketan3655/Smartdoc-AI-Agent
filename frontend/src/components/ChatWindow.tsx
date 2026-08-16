"use client";


import { useEffect, useState } from "react";
import {
  sendChat as apiSendChat,
  getChatHistory,
} from "../lib/api";
type Source = {
  page: string | null;
  text: string;
};

type SendChatResponse = {
  session_id?: string;
  answer: string;
  sources?: Source[];
};

async function sendChatRequest(
  documentId: string,
  message: string,
  sessionId?: string
): Promise<SendChatResponse> {
  return apiSendChat(
    documentId,
    message,
    sessionId
  );
}

type Message = {
  role: "user" | "assistant";
  content: string;
  sources?: Source[];
};

type ChatWindowProps = {
  documentId: string;
};

export default function ChatWindow({
  documentId,
}: ChatWindowProps) {
  const [messages, setMessages] = useState<Message[]>(
    []
  );

  const [input, setInput] = useState("");

  const [sessionId, setSessionId] =
    useState<string | null>(null);

  const [loading, setLoading] = useState(false);
  useEffect(() => {
    async function loadChatHistory() {
      const savedSessionId = localStorage.getItem(
        `smartdoc-session-${documentId}`
      );

      if (!savedSessionId) {
        return;
      }

      try {
        const response = await getChatHistory(
          savedSessionId
        );

        setSessionId(savedSessionId);

        const restoredMessages: Message[] =
          response.messages.map(
            (message: {
              role: "user" | "assistant";
              content: string;
            }) => ({
              role: message.role,
              content: message.content,
            })
          );

        setMessages(restoredMessages);
      } catch (error) {
        console.error(
          "Failed to load chat history:",
          error
        );

        localStorage.removeItem(
          `smartdoc-session-${documentId}`
        );
      }
    }

    loadChatHistory();
  }, [documentId]);

  async function handleSend() {
    const message = input.trim();

    if (!message || loading) {
      return;
    }

    const userMessage: Message = {
      role: "user",
      content: message,
    };

    setMessages((previous) => [
      ...previous,
      userMessage,
    ]);

    setInput("");
    setLoading(true);

    try {
      const response =
        await sendChatRequest(
          documentId,
          message,
          sessionId || undefined
        );

      if (response.session_id) {
        setSessionId(response.session_id);

        localStorage.setItem(
          `smartdoc-session-${documentId}`,
          response.session_id
        );
      }

      const assistantMessage: Message = {
        role: "assistant",
        content: response.answer,
        sources: response.sources || [],
      };

      setMessages((previous) => [
        ...previous,
        assistantMessage,
      ]);
    } catch (error) {
      console.error(error);

      setMessages((previous) => [
        ...previous,
        {
          role: "assistant",
          content:
            "Sorry, something went wrong. Please try again.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  }

  function handleKeyDown(
    event: React.KeyboardEvent
  ) {
    if (
      event.key === "Enter" &&
      !event.shiftKey
    ) {
      event.preventDefault();
      handleSend();
    }
  }

  function startNewChat() {
    localStorage.removeItem(
      `smartdoc-session-${documentId}`
    );

    setMessages([]);
    setSessionId(null);
  }
  return (
    <div className="flex h-full w-full flex-col">

      {/* Header */}

      <div className="flex items-center justify-between border-b border-slate-800 px-5 py-3">

        <div>
          <p className="text-sm font-medium text-white">
            Document Chat
          </p>

          {sessionId && (
            <p className="text-xs text-slate-500">
              Conversation active
            </p>
          )}
        </div>

        <button
          onClick={startNewChat}
          className="rounded-lg border border-slate-700 px-3 py-2 text-sm text-slate-400 hover:bg-slate-800 hover:text-white"
        >
          + New Chat
        </button>

      </div>

      {/* Messages */}

      <div className="flex-1 space-y-4 overflow-y-auto p-6">

        {messages.length === 0 && (
          <div className="flex h-full items-center justify-center">

            <div className="text-center">

              <div className="mb-4 text-5xl">
                🤖
              </div>

              <h2 className="text-2xl font-semibold">
                Ask your document
              </h2>

              <p className="mt-2 text-slate-400">
                Ask anything about the selected
                document.
              </p>

            </div>

          </div>
        )}

        {messages.map(
          (message, index) => (

            <div
              key={index}
              className={`flex ${message.role === "user"
                ? "justify-end"
                : "justify-start"
                }`}
            >

              <div
                className={`max-w-2xl rounded-2xl px-5 py-3 ${message.role === "user"
                  ? "bg-blue-600 text-white"
                  : "bg-slate-800 text-slate-100"
                  }`}
              >

                <div className="mb-1 text-xs font-medium opacity-60">

                  {message.role === "user"
                    ? "You"
                    : "SmartDoc AI"}

                </div>

                <p className="whitespace-pre-wrap text-sm leading-6">
                  {message.content}
                </p>

                {/* Sources */}

                {message.role === "assistant" &&
                  message.sources &&
                  message.sources.length > 0 && (

                    <div className="mt-4">

                      <p className="mb-2 text-xs font-semibold uppercase tracking-wide text-slate-500">
                        Sources
                      </p>

                      <div className="space-y-2">

                        {message.sources.map(
                          (
                            source,
                            sourceIndex
                          ) => (

                            <div
                              key={sourceIndex}
                              className="rounded-lg bg-slate-900 p-3"
                            >

                              <p className="mb-1 text-xs font-medium text-blue-400">
                                Page{" "}
                                {source.page ??
                                  "Unknown"}
                              </p>

                              <p className="line-clamp-3 text-xs leading-5 text-slate-400">
                                {source.text}
                              </p>

                            </div>

                          )
                        )}

                      </div>

                    </div>

                  )}

              </div>

            </div>

          )
        )}

        {/* Loading */}

        {loading && (
          <div className="flex justify-start">

            <div className="rounded-2xl bg-slate-800 px-5 py-3 text-sm text-slate-400">

              SmartDoc AI is thinking...

            </div>

          </div>
        )}

      </div>

      {/* Input */}

      <div className="border-t border-slate-800 p-5">

        <div className="mx-auto flex max-w-4xl gap-3">

          <textarea
            value={input}
            onChange={(event) =>
              setInput(event.target.value)
            }
            onKeyDown={handleKeyDown}
            placeholder="Ask something about your document..."
            rows={1}
            className="flex-1 resize-none rounded-xl border border-slate-700 bg-slate-900 px-4 py-3 text-sm text-white outline-none placeholder:text-slate-500 focus:border-blue-500"
          />

          <button
            onClick={handleSend}
            disabled={
              loading || !input.trim()
            }
            className="rounded-xl bg-blue-600 px-6 py-3 font-medium transition hover:bg-blue-500 disabled:cursor-not-allowed disabled:opacity-50"
          >
            Send
          </button>

        </div>

        <p className="mt-2 text-center text-xs text-slate-600">
          Enter to send · Shift + Enter for new line
        </p>

      </div>

    </div>
  );
}
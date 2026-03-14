"use client"

import { useState } from "react"

export default function Home() {

  const API = process.env.NEXT_PUBLIC_API_URL

  const [url, setUrl] = useState("")
  const [result, setResult] = useState("")
  const [loading, setLoading] = useState(false)

  const analyzeVideo = async () => {

    if (!url) return

    setLoading(true)
    setResult("")

    try {

      const res = await fetch(`${API}/analyze`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ url })
      })

      const data = await res.json()

      setResult(data.explanation)

    } catch (error) {

      setResult("Error analyzing video.")

    }

    setLoading(false)
  }

  return (

    <main className="min-h-screen bg-gray-950 text-white flex items-center justify-center p-6">

      <div className="w-full max-w-3xl space-y-8">

        <div className="text-center space-y-2">
          <h1 className="text-4xl font-bold">
            YouTube AI Explainer
          </h1>

          <p className="text-gray-400">
            Paste a YouTube link and let AI explain the topic
          </p>
        </div>

        <div className="flex gap-2">

          <input
            type="text"
            placeholder="https://youtube.com/..."
            value={url}
            onChange={(e)=>setUrl(e.target.value)}
            className="flex-1 px-4 py-3 rounded-lg bg-gray-900 border border-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />

          <button
            onClick={analyzeVideo}
            className="px-5 py-3 rounded-lg bg-blue-600 hover:bg-blue-700 transition"
          >
            Analyze
          </button>

        </div>

        {loading && (
          <div className="text-center text-gray-400">
            Analyzing video...
          </div>
        )}

        {result && (

          <div className="bg-gray-900 border border-gray-800 rounded-xl p-6">

            <h2 className="text-xl font-semibold mb-4">
              AI Explanation
            </h2>

            <div className="whitespace-pre-wrap text-gray-200 leading-relaxed">
              {result}
            </div>

          </div>

        )}

      </div>

    </main>

  )
}

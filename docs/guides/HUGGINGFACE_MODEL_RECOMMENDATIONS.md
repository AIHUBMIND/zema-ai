# Hugging Face Model Recommendations for Zema AI

## File Location
`docs/guides/HUGGINGFACE_MODEL_RECOMMENDATIONS.md`

## Purpose
Recommendations for Hugging Face models suitable for Zema AI voice chat and multilingual support, especially for Ethiopian languages.

## Current Stack
- **STT**: Faster Whisper (uses Hugging Face Whisper models)
- **TTS**: Piper TTS (offline, fast)
- **LLM**: Ollama with Llama models (local inference)

---

## 🎤 Speech-to-Text (STT) Models

### Current: Faster Whisper (Hugging Face)
**Model**: `openai/whisper-*` series
- ✅ Already using these via faster-whisper
- ✅ Excellent multilingual support (99+ languages including Amharic)
- ✅ Best accuracy for offline use

### Recommended Hugging Face STT Models:

#### 1. **openai/whisper-large-v3** (BEST Quality)
- **Why**: Highest accuracy, supports Amharic perfectly
- **Size**: ~3GB
- **Use Case**: Best quality when accuracy matters most
- **Hugging Face**: https://huggingface.co/openai/whisper-large-v3

#### 2. **openai/whisper-medium** (BALANCED)
- **Why**: Good balance of accuracy and speed
- **Size**: ~1.5GB
- **Use Case**: Recommended for most users
- **Hugging Face**: https://huggingface.co/openai/whisper-medium

#### 3. **openai/whisper-base** (FASTEST)
- **Why**: Fastest, good enough accuracy
- **Size**: ~150MB
- **Use Case**: Low-resource systems, real-time needs
- **Hugging Face**: https://huggingface.co/openai/whisper-base

#### 4. **Systran/faster-whisper-large-v3** (OPTIMIZED)
- **Why**: Optimized version of Whisper, faster inference
- **Size**: ~3GB
- **Use Case**: When you need Whisper quality but faster
- **Hugging Face**: https://huggingface.co/Systran/faster-whisper-large-v3

### For Ethiopian Languages:
- ✅ **Amharic**: Fully supported by all Whisper models
- ✅ **Tigrinya**: Supported by Whisper Large
- ✅ **Oromo**: Supported by Whisper Large
- ✅ **Somali**: Supported by Whisper Large

---

## 🔊 Text-to-Speech (TTS) Models

### Current: Piper TTS
- ✅ Offline, fast, lightweight
- ⚠️ Limited Ethiopian language voices

### Recommended Hugging Face TTS Models:

#### 1. **microsoft/speecht5_tts** (MULTILINGUAL)
- **Why**: Good multilingual support, natural voices
- **Languages**: English, Amharic (via fine-tuning)
- **Size**: ~500MB
- **Use Case**: When you need better voice quality
- **Hugging Face**: https://huggingface.co/microsoft/speecht5_tts

#### 2. **coqui/XTTS-v2** (BEST MULTILINGUAL)
- **Why**: Excellent multilingual, voice cloning
- **Languages**: 17+ languages including Amharic
- **Size**: ~1.8GB
- **Use Case**: Best quality multilingual TTS
- **Hugging Face**: https://huggingface.co/coqui/XTTS-v2

#### 3. **facebook/mms-tts** (Meta Multilingual)
- **Why**: 1100+ languages, including Ethiopian languages
- **Size**: ~2GB per language
- **Use Case**: Maximum language coverage
- **Hugging Face**: https://huggingface.co/facebook/mms-tts

#### 4. **RiteshAI/piper-tts** (PIPER ALTERNATIVE)
- **Why**: If you want to stick with Piper but get from Hugging Face
- **Languages**: English, Amharic (community models)
- **Size**: ~50MB per voice
- **Use Case**: Lightweight alternative

### For Ethiopian Languages:
- **Amharic**: XTTS-v2, MMS-TTS (best options)
- **Tigrinya**: MMS-TTS
- **Oromo**: MMS-TTS
- **Somali**: MMS-TTS

---

## 🧠 Multilingual LLM Models (Ollama-Compatible)

### Current: Llama 2/3 (English-focused)
- ✅ Good for English
- ⚠️ Limited multilingual capabilities

### Recommended Ollama-Compatible Models:

#### 1. **Qwen 2.5** (BEST MULTILINGUAL)
- **Why**: Excellent multilingual, supports 100+ languages including Amharic
- **Models**: `qwen2.5:7b`, `qwen2.5:14b`, `qwen2.5:72b`
- **Ollama**: `ollama pull qwen2.5:7b`
- **Use Case**: Best balance of quality and multilingual support
- **Hugging Face**: https://huggingface.co/Qwen/Qwen2.5-7B-Instruct

#### 2. **Mistral 7B** (GOOD MULTILINGUAL)
- **Why**: Good multilingual, smaller than Qwen
- **Models**: `mistral:7b`, `mixtral:8x7b`
- **Ollama**: `ollama pull mistral:7b`
- **Use Case**: Fast multilingual responses
- **Hugging Face**: https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.2

#### 3. **Aya (Cohere)** (TRANSLATION SPECIALIST)
- **Why**: Specifically designed for translation, 100+ languages
- **Models**: `aya:8b`, `aya:35b`
- **Ollama**: `ollama pull aya:8b`
- **Use Case**: Translation between languages
- **Hugging Face**: https://huggingface.co/CohereForAI/aya-8b

#### 4. **Llama 3.1** (IMPROVED MULTILINGUAL)
- **Why**: Better multilingual than Llama 2/3
- **Models**: `llama3.1:8b`, `llama3.1:70b`
- **Ollama**: `ollama pull llama3.1:8b`
- **Use Case**: If you want to stay with Llama family
- **Hugging Face**: https://huggingface.co/meta-llama/Meta-Llama-3.1-8B-Instruct

### Translation Capabilities:
- **Qwen 2.5**: ✅ Excellent translation (English ↔ Amharic, etc.)
- **Aya**: ✅ Best for translation tasks
- **Mistral**: ✅ Good translation
- **Llama 3.1**: ⚠️ Moderate translation (better than Llama 2/3)

---

## 🎯 Recommended Stack for Zema AI

### For Voice Chat (Best Quality):
1. **STT**: `openai/whisper-medium` (via faster-whisper) ✅ Already using
2. **TTS**: `coqui/XTTS-v2` (upgrade from Piper for better multilingual)
3. **LLM**: `qwen2.5:7b` (best multilingual support)

### For Multilingual/Ethiopian Support:
1. **STT**: `openai/whisper-large-v3` (best Amharic/Tigrinya recognition)
2. **TTS**: `facebook/mms-tts` (1100+ languages including Ethiopian)
3. **LLM**: `qwen2.5:7b` or `aya:8b` (excellent translation)

### For Resource-Constrained (Mini PC):
1. **STT**: `openai/whisper-base` (fastest, still good)
2. **TTS**: `piper-tts` (current, lightweight) ✅ Already using
3. **LLM**: `qwen2.5:3b` (smaller multilingual model)

---

## 📋 Implementation Recommendations

### Priority 1: Upgrade LLM to Qwen 2.5
**Why**: Better multilingual and translation
**Action**: 
```bash
ollama pull qwen2.5:7b
# Update settings: llm_model = "qwen2.5:7b"
```

### Priority 2: Test XTTS-v2 for TTS
**Why**: Better multilingual voices, especially Ethiopian
**Action**: Evaluate XTTS-v2 vs current Piper for Amharic quality

### Priority 3: Consider Whisper Large for STT
**Why**: Better accuracy for Ethiopian languages
**Action**: Test `whisper-large-v3` vs current `whisper-base`

---

## 🔗 Useful Hugging Face Links

- **Whisper Models**: https://huggingface.co/openai/whisper-large-v3
- **XTTS-v2**: https://huggingface.co/coqui/XTTS-v2
- **MMS-TTS**: https://huggingface.co/facebook/mms-tts
- **Qwen 2.5**: https://huggingface.co/Qwen/Qwen2.5-7B-Instruct
- **Aya**: https://huggingface.co/CohereForAI/aya-8b

---

## 🌍 Language Support Matrix

| Model Type | English | Amharic | Tigrinya | Oromo | Somali | Translation |
|------------|---------|---------|----------|-------|--------|-------------|
| Whisper Base | ✅ | ✅ | ⚠️ | ⚠️ | ⚠️ | N/A |
| Whisper Large | ✅ | ✅ | ✅ | ✅ | ✅ | N/A |
| Piper TTS | ✅ | ⚠️ | ❌ | ❌ | ❌ | N/A |
| XTTS-v2 | ✅ | ✅ | ⚠️ | ⚠️ | ⚠️ | N/A |
| MMS-TTS | ✅ | ✅ | ✅ | ✅ | ✅ | N/A |
| Llama 2/3 | ✅ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ |
| Qwen 2.5 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Aya | ✅ | ✅ | ✅ | ✅ | ✅ | ✅✅ |

**Legend**: ✅ Excellent | ⚠️ Moderate | ❌ Limited/None

---

## 💡 Key Insights

1. **For Voice Chat**: Faster Whisper (already using) + XTTS-v2 + Qwen 2.5
2. **For Multilingual**: Whisper Large + MMS-TTS + Qwen 2.5 or Aya
3. **For Translation**: Qwen 2.5 or Aya models (both excellent)
4. **For Resource Constraints**: Current stack (Whisper Base + Piper + smaller Qwen)

---

## 🚀 Next Steps

1. **Test Qwen 2.5**: `ollama pull qwen2.5:7b` and test multilingual
2. **Evaluate XTTS-v2**: Compare with Piper for Amharic quality
3. **Consider Whisper Large**: Test accuracy improvement for Ethiopian languages
4. **Add Translation Feature**: Use Qwen/Aya for language translation

---

**Last Updated**: 2025-11-03  
**Source**: Hugging Face Model Hub (https://huggingface.co/)


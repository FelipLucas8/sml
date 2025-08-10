<template>
  <div class="main d-flex">
    <!-- Main Content -->
    <v-container class="pa-6">
      <v-row>
        <!-- Left Panel - Model Configuration -->
        <v-col cols="12" md="4">
          <v-card class="custom-dark-surface mb-4" elevation="3">
            <v-card-title class="d-flex align-center title">
              <v-icon class="mr-2">mdi-cog</v-icon>
              Model Configuration
            </v-card-title>
            <v-card-text class="text">
              <v-select v-model="selectedModel" :items="models" item-title="name" item-value="id" label="Select Model"
                variant="outlined" density="comfortable" prepend-inner-icon="mdi-robot"
                @update:modelValue="setParameters">
                <template v-slot:item="{ props, item }">
                  <v-list-item v-bind="props">
                    <template v-slot:prepend>
                      <span :class="`status-indicator status-\${item.raw.status}`"></span>
                    </template>
                    <v-list-item-title>{{ item.raw.name }}</v-list-item-title>
                    <v-list-item-subtitle>{{ item.raw.size }}</v-list-item-subtitle>
                  </v-list-item>
                </template>
              </v-select>

              <v-divider class="my-4"></v-divider>

              <v-row>
                <v-col cols="6">
                  <v-text-field v-model.number="modelConfig.temperature" label="Temperature" type="number" step="0.1"
                    min="0" max="2" variant="outlined" density="compact"></v-text-field>
                </v-col>
                <v-col cols="6">
                  <v-text-field v-model.number="modelConfig.maxTokens" label="Max Tokens" type="number"
                    variant="outlined" density="compact"></v-text-field>
                </v-col>
              </v-row>

              <v-row>
                <v-col cols="6">
                  <v-text-field v-model.number="modelConfig.topP" label="Top P" type="number" step="0.1" min="0" max="1"
                    variant="outlined" density="compact"></v-text-field>
                </v-col>
                <v-col cols="6">
                  <v-text-field v-model.number="modelConfig.topK" label="Top K" type="number" variant="outlined"
                    density="compact"></v-text-field>
                </v-col>
              </v-row>

              <v-textarea v-model="systemPrompt" label="System Prompt" variant="outlined" rows="3"
                placeholder="Enter system instructions..."></v-textarea>
            </v-card-text>
          </v-card>

          <!-- Performance Metrics -->
          <v-card class="custom-dark-surface metrics-card" elevation="3">
            <v-card-title class="d-flex align-center title">
              <v-icon class="mr-2">mdi-chart-line</v-icon>
              Performance Metrics
            </v-card-title>
            <v-card-text>
              <v-row>
                <v-col cols="6">
                  <div class="text-caption text-grey">Response Time</div>
                  <div class="text-h6 text">{{ metrics.responseTime }}s</div>
                </v-col>
                <v-col cols="6">
                  <div class="text-caption text-grey">Tokens/sec</div>
                  <div class="text-h6 text">{{ metrics.tokensPerSecond }}</div>
                </v-col>
              </v-row>
              <v-row>
                <v-col cols="6">
                  <div class="text-caption text-grey">Input Tokens</div>
                  <div class="text-body-2 token-counter">{{ metrics.inputTokens }}</div>
                </v-col>
                <v-col cols="6">
                  <div class="text-caption text-grey">Output Tokens</div>
                  <div class="text-body-2 token-counter">{{ metrics.outputTokens }}</div>
                </v-col>
              </v-row>
              <v-progress-linear :model-value="metrics.gpuUtilization" color="primary" height="6"
                class="mt-3"></v-progress-linear>
              <div class="text-caption text-grey mt-1">GPU Utilization: {{ metrics.gpuUtilization }}%</div>
            </v-card-text>
          </v-card>
        </v-col>

        <!-- Right Panel - Testing Interface -->
        <v-col cols="12" md="8">
          <v-card class="custom-dark-surface" elevation="3" height="100%">
            <v-card-title class="d-flex align-center justify-space-between">
              <div class="d-flex align-center title">
                <v-icon class="mr-2">mdi-message-text</v-icon>
                Conversation
              </div>
              <div>
                <v-btn variant="outlined" size="small" class="mr-2" color="primary" prepend-icon="mdi-content-save"
                  @click="saveSession">
                  Save Session
                </v-btn>
                <v-btn variant="outlined" size="small" color="error" prepend-icon="mdi-delete"
                  @click="clearConversation">
                  Clear
                </v-btn>
              </div>
            </v-card-title>

            <v-divider></v-divider>

            <!-- Chat History -->
            <v-card-text class="pa-0" style="height: 400px; overflow-y: auto;" ref="chatContainer">
              <div class="pa-4">
                <v-timeline density="compact" side="end">
                  <v-timeline-item v-for="(message, i) in messages" :key="i"
                    :dot-color="message.role === 'user' ? 'primary' : 'success'" size="small">
                    <template v-slot:icon>
                      <v-icon :icon="message.role === 'user' ? 'mdi-account' : 'mdi-robot'"></v-icon>
                    </template>
                    <v-card :class="message.role === 'user' ? 'custom-darker-surface' : 'custom-dark-surface'"
                      variant="flat">
                      <v-card-text class="py-2">
                        <div class="text-caption text-grey mb-1">
                          {{ message.role === 'user' ? 'You' : 'Assistant' }} • {{ message.timestamp }}
                        </div>
                        <div class="text-body-2">{{ message.content }}</div>
                      </v-card-text>
                    </v-card>
                  </v-timeline-item>
                </v-timeline>

                <div v-if="messages.length === 0" class="text-center text-grey py-8">
                  <v-icon size="64" class="mb-4">mdi-chat-outline</v-icon>
                  <div class="text-h6">Start a conversation</div>
                  <div class="text-body-2">Enter your prompt below to begin testing</div>
                </div>
              </div>
            </v-card-text>

            <v-divider></v-divider>

            <!-- Input Area -->
            <v-card-text>
              <v-textarea v-model="userInput" label="Enter your prompt..." variant="outlined" rows="4" auto-grow
                placeholder="Type your message here..." :loading="isGenerating" class="text">
                <template v-slot:append-inner>
                  <div class="text-caption text-grey token-counter">
                    {{ inputCharCount }} chars
                  </div>
                </template>
              </v-textarea>

              <div class="d-flex justify-space-between align-center mt-4">
                <div class="d-flex align-center">
                  <v-chip size="small" variant="outlined" class="mr-2" prepend-icon="mdi-clock-outline"
                    :color="streamingEnabled ? 'success' : 'grey'">
                    Streaming: {{ streamingEnabled ? 'ON' : 'OFF' }}
                  </v-chip>
                  <v-chip size="small" variant="outlined" :color="selectedModel ? 'success' : 'error'"
                    :prepend-icon="selectedModel ? 'mdi-check' : 'mdi-alert'">
                    Model: {{ selectedModelName }}
                  </v-chip>
                </div>

                <div class="d-flex">
                  <v-btn variant="outlined" class="mr-2" prepend-icon="mdi-stop" :disabled="!isGenerating" color="error"
                    @click="stopGeneration">
                    Stop
                  </v-btn>
                  <v-btn color="primary" :loading="isGenerating" :disabled="!canSendMessage" append-icon="mdi-send"
                    @click="sendMessage">
                    Generate
                  </v-btn>
                </div>
              </div>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>

      <!-- Quick Actions -->
      <v-row class="mt-4">
        <v-col cols="12">
          <v-card class="custom-dark-surface" elevation="3">
            <v-card-title class="d-flex align-center title">
              <v-icon class="mr-2">mdi-lightning-bolt</v-icon>
              Quick Test Scenarios
            </v-card-title>
            <v-card-text>
              <v-row>
                <v-col cols="12" sm="6" md="3" v-for="(scenario, i) in quickScenarios" :key="i">
                  <v-card class="model-card custom-darker-surface" variant="outlined" hover
                    @click="loadScenario(scenario)">
                    <v-card-text class="text-center pa-4">
                      <v-icon size="32" class="mb-2" :color="scenario.color">{{ scenario.icon }}</v-icon>
                      <div class="text-subtitle-2 font-weight-bold title">{{ scenario.title }}</div>
                      <div class="text-caption text-grey mt-1">{{ scenario.description }}</div>
                    </v-card-text>
                  </v-card>
                </v-col>
              </v-row>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
import { ref, reactive, computed, watch, onMounted } from 'vue'
import { RepositoryFactory } from '@/repositories/repositoryFactory/repositoryFactory';

const modelRepository = RepositoryFactory.get("models");

export default {
  setup() {
    // Reactive state
    const selectedModel = ref('');
    const userInput = ref('');
    const systemPrompt = ref(`You must to summarize the user content, keep the main points to avoid lose information.Keep in mind that the goal is to extract the main ideia to use in another LLM calls, you must to have a content that cut the prompt cost as much as possible`);
    // put in the User prompt directly:  Summarize the following chat history to retain important user intent, questions, and assistant responses. Keep technical context and reduce redundancy. This summary will be used as input for further conversation, so maintain flow and clarity The summary must be shorter than the original version. Chat History: User: I need help connecting Vue to Flask. Assistant: You can use Flask-SocketIO and socket.io-client in Vue. User: How can I stream chat messages in real-time? Assistant: Use WebSockets for full-duplex communication. Here's an example...
    const isGenerating = ref(false);
    const streamingEnabled = ref(true);
    const chatContainer = ref(null);

    // Model configuration using reactive
    const modelConfig = reactive({
      temperature: 0.7,
      maxTokens: 2048,
      topP: 0.9,
      topK: 40
    });

    // Performance metrics
    const metrics = reactive({
      responseTime: 1.2,
      tokensPerSecond: 45.3,
      inputTokens: 0,
      outputTokens: 0,
      gpuUtilization: 75
    });

    // Messages array
    const messages = ref([
      {
        role: 'user',
        content: 'Hello! Can you help me test this language model interface?',
        timestamp: '10:30 AM'
      },
      {
        role: 'assistant',
        content: 'Hello! I\'d be happy to help you test this interface. This is a sample response to demonstrate how the conversation flow works. You can ask me anything!',
        timestamp: '10:30 AM'
      }
    ]);

    // Available models
    const models = ref([
      { id: 'Phi-3-mini-4k-instruct-q4.gguf', name: 'Phi-3-mini', size: '3.8B params', status: 'ready' }
    ]);

    const modelsParameter = ref([
      { id: 'Phi-3-mini-4k-instruct-q4.gguf', temperature: 0.3, max_tokens: 100, top_p: 0.95, top_k: 40 }
    ]);

    // Quick scenarios
    const quickScenarios = ref([
      {
        title: 'Creative Writing',
        description: 'Test creative storytelling abilities',
        icon: 'mdi-feather',
        color: 'purple',
        prompt: 'Write a short creative story about a robot discovering emotions for the first time.'
      },
      {
        title: 'Code Generation',
        description: 'Test programming capabilities',
        icon: 'mdi-code-tags',
        color: 'green',
        prompt: 'Write a Python function that implements a binary search algorithm with proper error handling.'
      },
      {
        title: 'Analysis',
        description: 'Test analytical reasoning',
        icon: 'mdi-chart-bar',
        color: 'orange',
        prompt: 'Analyze the pros and cons of renewable energy sources versus traditional fossil fuels.'
      },
      {
        title: 'Math & Logic',
        description: 'Test mathematical reasoning',
        icon: 'mdi-calculator',
        color: 'blue',
        prompt: 'Solve this step by step: If a train travels 120 miles in 2 hours, and then 180 miles in 3 hours, what is its average speed for the entire journey?'
      }
    ]);

    // Computed properties
    const inputCharCount = computed(() => userInput.value.length);

    const selectedModelName = computed(() => {
      if (!selectedModel.value) return 'None';
      const model = models.value.find(m => m.id === selectedModel.value);
      return model ? model.name : 'Unknown';
    });

    const canSendMessage = computed(() => {
      return userInput.value.trim() && selectedModel.value && !isGenerating.value;
    });

    // Methods
    const sendMessage = async () => {
      if (!canSendMessage.value) return;

      isGenerating.value = true;
      metrics.inputTokens = Math.floor(userInput.value.length / 4);

      // Add user message
      messages.value.push({
        role: 'user',
        content: userInput.value,
        timestamp: getCurrentTime()
      });

      const currentInput = userInput.value;
      userInput.value = '';

      // Scroll to bottom
      // await nextTick();
      scrollToBottom();

      // Simulate API call - Replace with actual SLLM API call
      try {
        // await simulateAPICall(currentInput);
        const modelResponse = await modelRepository.getModelResponse(currentInput, selectedModel.value, systemPrompt.value, modelConfig.temperature, modelConfig.maxTokens, modelConfig.topP, modelConfig.topK)

        if (modelResponse.status == 200) {
          messages.value.push({
            role: 'assistant',
            content: modelResponse.data,
            timestamp: getCurrentTime()
          });
        }
      } catch (error) {
        console.error('Error generating response:', error);
        messages.value.push({
          role: 'assistant',
          content: 'Sorry, there was an error generating the response. Please try again.',
          timestamp: getCurrentTime()
        });
      } finally {
        isGenerating.value = false;
      }
    };

    const simulateAPICall = async (input) => {
      return new Promise((resolve) => {
        setTimeout(() => {
          messages.value.push({
            role: 'assistant',
            content: `This is a simulated response from the SLLM (${selectedModelName.value}). In a real implementation, this would be the actual model response based on your input: "${input.substring(0, 50)}${input.length > 50 ? '...' : ''}" and the current configuration.`,
            timestamp: getCurrentTime()
          });
          metrics.outputTokens = Math.floor(Math.random() * 200) + 50;
          metrics.responseTime = +(Math.random() * 3 + 0.5).toFixed(1);
          metrics.tokensPerSecond = +(metrics.outputTokens / metrics.responseTime).toFixed(1);
          resolve();
        }, 2000);
      });
    };

    const stopGeneration = () => {
      isGenerating.value = false;
      // In real implementation, cancel the API request here
    };

    const clearConversation = () => {
      messages.value = [];
      metrics.inputTokens = 0;
      metrics.outputTokens = 0;
    };

    const saveSession = () => {
      const sessionData = {
        messages: messages.value,
        modelConfig: { ...modelConfig },
        selectedModel: selectedModel.value,
        systemPrompt: systemPrompt.value,
        timestamp: new Date().toISOString()
      };

      // In real implementation, save to backend or download as file
      console.log('Session saved:', sessionData);

      // Create and download JSON file
      const blob = new Blob([JSON.stringify(sessionData, null, 2)], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `sllm-session-${Date.now()}.json`;
      a.click();
      URL.revokeObjectURL(url);
    };

    const loadScenario = (scenario) => {
      userInput.value = scenario.prompt;
    };

    const getCurrentTime = () => {
      return new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    };

    const scrollToBottom = () => {
      if (chatContainer.value) {
        chatContainer.value.scrollTop = chatContainer.value.scrollHeight;
      }
    };

    const setParameters = (item) => {
      var selectedModelParameter = modelsParameter.value.find(m => m.id === selectedModel.value)
      if (selectedModelParameter) {
        modelConfig.temperature = selectedModelParameter.temperature
        modelConfig.maxTokens = selectedModelParameter.max_tokens
        modelConfig.topP = selectedModelParameter.top_p
        modelConfig.topK = selectedModelParameter.top_k
      }
    }

    // expose to template and other options API hooks
    // Watch for new messages and scroll to bottom
    watch(messages, async () => {
      await nextTick();
      scrollToBottom();
    }, { deep: true });

    // Watch model config changes
    watch(modelConfig, (newConfig) => {
      console.log('Model config updated:', newConfig);
    }, { deep: true });

    // Lifecycle
    onMounted(() => {
      selectedModel.value = modelsParameter.value[0].id
      modelConfig.temperature = modelsParameter.value[0].temperature
      modelConfig.maxTokens = modelsParameter.value[0].max_tokens
      modelConfig.topP = modelsParameter.value[0].top_p
      modelConfig.topK = modelsParameter.value[0].top_k
      // console.log('SLLM Testing Interface mounted', modelsParameter.value[0]);
    });

    return {
      // State
      selectedModel,
      userInput,
      systemPrompt,
      isGenerating,
      streamingEnabled,
      modelConfig,
      metrics,
      messages,
      models,
      quickScenarios,
      chatContainer,
      setParameters,

      // Computed
      inputCharCount,
      selectedModelName,
      canSendMessage,

      // Methods
      sendMessage,
      stopGeneration,
      clearConversation,
      saveSession,
      loadScenario
    };
  },

  mounted() {
    console.log(this.count) // 0
  }
}
</script>

<style>
.main {
  width: 1200px;
}

.v-application {
  background: #121212 !important;
}

.custom-dark-surface {
  background-color: #1e1e1e !important;
}

.custom-darker-surface {
  background-color: #0d1117 !important;
}

.gradient-header {
  background: linear-gradient(135deg, #2c2c2c 0%, #1a1a1a 100%);
}

.response-area {
  border: 1px solid #333;
  background-color: #1a1a1a;
}

.model-card {
  transition: all 0.3s ease;
}

.model-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
}

.status-indicator {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  display: inline-block;
  margin-right: 8px;
}

.status-ready {
  background-color: #4caf50;
}

.status-busy {
  background-color: #ff9800;
}

.status-error {
  background-color: #f44336;
}

.metrics-card {
  border-left: 4px solid #2196f3;
}

.token-counter {
  font-family: 'Courier New', monospace;
  font-size: 0.9em;
}

.title {
  color: white;
}

.text {
  color: white;
}

.text-body-2 {
  color: white;
}
</style>
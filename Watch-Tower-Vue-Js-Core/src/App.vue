<template>
  <div class="min-h-screen bg-black relative overflow-hidden">
    <Navbar />
    <router-view />
    
    <div class="absolute inset-0 opacity-30">
      <div class="absolute top-0 left-0 w-full h-full bg-[linear-gradient(rgba(0,255,255,0.03)_1px,transparent_1px),linear-gradient(90deg,rgba(0,255,255,0.03)_1px,transparent_1px)] bg-[size:40px_40px]"></div>
    </div>

    <div class="absolute inset-0 pointer-events-none overflow-hidden">
      <div class="absolute top-0 left-0 w-full h-[2px] bg-gradient-to-r from-transparent via-cyan-500/30 to-transparent animate-scanX"></div>
      <div class="absolute top-0 left-0 w-[2px] h-full bg-gradient-to-b from-transparent via-cyan-500/30 to-transparent animate-scanY"></div>
    </div>

    <div class="absolute inset-0 pointer-events-none">
      <div class="absolute top-[20%] left-[15%] w-1 h-1 bg-cyan-400/40 rounded-full animate-float1"></div>
      <div class="absolute top-[60%] left-[85%] w-1.5 h-1.5 bg-blue-400/30 rounded-full animate-float2"></div>
      <div class="absolute top-[80%] left-[25%] w-1 h-1 bg-cyan-300/40 rounded-full animate-float3"></div>
      <div class="absolute top-[40%] left-[75%] w-0.5 h-0.5 bg-white/30 rounded-full animate-float4"></div>
      <div class="absolute top-[30%] left-[45%] w-1 h-1 bg-cyan-500/30 rounded-full animate-float5"></div>
    </div>

    <div class="fixed top-0 left-0 right-0 h-[1px] bg-gradient-to-r from-transparent via-cyan-500/50 to-transparent z-20 shadow-[0_0_10px_rgba(0,255,255,0.3)]"></div>
  </div>

  <div v-if="showModal" class="fixed inset-0 z-50 flex items-center justify-center px-4" @click.self="closeModal">
    <div class="absolute inset-0 bg-black/80 backdrop-blur-md"></div>
    
    <div class="relative bg-gradient-to-br from-gray-900 to-black border border-cyan-500/30 rounded-2xl max-w-md w-full p-8 shadow-2xl shadow-cyan-500/20 animate-modalIn">
      <div class="absolute -inset-0.5 bg-gradient-to-r from-cyan-500 to-blue-600 rounded-2xl blur opacity-30"></div>
      
      <div class="relative">
        <button @click="closeModal" class="absolute -top-2 -right-2 text-gray-500 hover:text-gray-300 transition-colors">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
          </svg>
        </button>

        <div class="flex justify-center mb-6">
          <div class="w-16 h-16 rounded-full bg-gradient-to-br from-cyan-500/20 to-blue-600/20 flex items-center justify-center border border-cyan-500/30">
            <svg class="w-8 h-8 text-cyan-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
            </svg>
          </div>
        </div>

        <h3 class="text-2xl font-bold text-center text-white mb-3">Under Development</h3>
        
        <div class="w-12 h-px bg-gradient-to-r from-transparent via-cyan-500/50 to-transparent mx-auto mb-4"></div>
        
        <p class="text-gray-400 text-center leading-relaxed mb-6">
          This feature is currently in active development.<br>
          Our team is working hard to deliver an exceptional experience.
        </p>

        <div class="flex justify-center mb-6">
          <span class="px-3 py-1 bg-cyan-500/10 border border-cyan-500/20 rounded-full text-xs text-cyan-400 tracking-wider">
            COMING SOON
          </span>
        </div>

        <div class="w-full bg-gray-800 rounded-full h-1 mb-6 overflow-hidden">
          <div class="bg-gradient-to-r from-cyan-500 to-blue-500 h-1 rounded-full animate-progress" style="width: 65%"></div>
        </div>

        <button 
          @click="closeModal"
          class="w-full py-2.5 bg-transparent border border-cyan-500/40 text-cyan-400 text-sm uppercase tracking-wider rounded-lg hover:bg-cyan-500/10 transition-all duration-300"
        >
          Got it
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import Navbar from './components/layouts/partials/Navbar.vue' 

const showModal = ref(false)

const closeModal = () => {
  showModal.value = false
}

window.showDevelopmentModal = () => {
  showModal.value = true
}
</script>

<style scoped>
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes gradient {
  0%, 100% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
}

@keyframes rotateSlow {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

@keyframes rotateReverse {
  from { transform: rotate(360deg); }
  to { transform: rotate(0deg); }
}

@keyframes pulseRing {
  0%, 100% { opacity: 0.3; transform: scale(1); }
  50% { opacity: 0.1; transform: scale(1.05); }
}

@keyframes scanX {
  0% { transform: translateX(-100%); }
  100% { transform: translateX(100%); }
}

@keyframes scanY {
  0% { transform: translateY(-100%); }
  100% { transform: translateY(100%); }
}

@keyframes float1 {
  0%, 100% { transform: translate(0, 0); opacity: 0.3; }
  50% { transform: translate(20px, -20px); opacity: 0.8; }
}

@keyframes float2 {
  0%, 100% { transform: translate(0, 0); opacity: 0.2; }
  50% { transform: translate(-15px, -25px); opacity: 0.7; }
}

@keyframes float3 {
  0%, 100% { transform: translate(0, 0); opacity: 0.4; }
  50% { transform: translate(10px, 20px); opacity: 0.9; }
}

@keyframes float4 {
  0%, 100% { transform: translate(0, 0); opacity: 0.3; }
  50% { transform: translate(-20px, 15px); opacity: 0.8; }
}

@keyframes float5 {
  0%, 100% { transform: translate(0, 0); opacity: 0.2; }
  50% { transform: translate(15px, -15px); opacity: 0.7; }
}

@keyframes modalIn {
  from { opacity: 0; transform: scale(0.95) translateY(-20px); }
  to { opacity: 1; transform: scale(1) translateY(0); }
}

@keyframes progressBar {
  from { width: 0%; }
  to { width: 65%; }
}

.animate-fadeIn {
  animation: fadeIn 0.8s ease-out forwards;
  opacity: 0;
}

.animate-gradient {
  background-size: 200% auto;
  animation: gradient 3s ease infinite;
}

.animate-rotateSlow {
  animation: rotateSlow 30s linear infinite;
}

.animate-rotateReverse {
  animation: rotateReverse 25s linear infinite;
}

.animate-pulseRing {
  animation: pulseRing 4s ease-in-out infinite;
}

.animate-scanX {
  animation: scanX 6s linear infinite;
}

.animate-scanY {
  animation: scanY 8s linear infinite;
}

.animate-float1 { animation: float1 8s ease-in-out infinite; }
.animate-float2 { animation: float2 10s ease-in-out infinite; }
.animate-float3 { animation: float3 7s ease-in-out infinite; }
.animate-float4 { animation: float4 9s ease-in-out infinite; }
.animate-float5 { animation: float5 11s ease-in-out infinite; }

.animate-modalIn {
  animation: modalIn 0.3s ease-out;
}

.animate-progress {
  animation: progressBar 1.5s ease-out forwards;
}

.delay-100 { animation-delay: 0.1s; }
.delay-300 { animation-delay: 0.3s; }

.group-hover\:scale-x-100 {
  transform: scaleX(1);
}

::-webkit-scrollbar {
  width: 6px;
}

::-webkit-scrollbar-track {
  background: #1a1a1a;
}

::-webkit-scrollbar-thumb {
  background: #0ea5e9;
  border-radius: 3px;
}
</style>
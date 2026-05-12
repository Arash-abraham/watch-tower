<template>
    <div class="min-h-screen bg-black relative overflow-hidden">
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
      
      <div class="relative min-h-screen flex items-center justify-center">
        <div class="absolute top-1/4 left-1/4 w-64 h-64 border border-cyan-500/10 rotate-45 animate-rotateSlow">
          <div class="absolute inset-4 border border-cyan-500/5"></div>
          <div class="absolute inset-8 border border-cyan-500/5"></div>
        </div>
        
        <div class="absolute bottom-1/3 right-1/4 w-80 h-80 border border-cyan-500/10 rounded-full animate-pulseRing">
          <div class="absolute inset-8 border border-cyan-500/5 rounded-full"></div>
          <div class="absolute inset-16 border border-cyan-500/5 rounded-full"></div>
        </div>
        
        <div class="absolute top-1/2 right-1/3 w-32 h-32 border border-cyan-500/10 animate-rotateReverse">
          <div class="absolute inset-2 border border-cyan-500/5"></div>
        </div>
  
        <div class="absolute inset-0 bg-gradient-to-br from-transparent via-cyan-500/[0.03] to-transparent"></div>
        <div class="absolute inset-0 bg-gradient-to-tl from-transparent via-blue-500/[0.02] to-transparent"></div>
  
        <div class="relative z-10 max-w-6xl mx-auto px-6 py-20">
          <div class="text-center mb-12">
            <div class="inline-flex items-center gap-3 px-4 py-2 border border-cyan-500/20 bg-cyan-500/5 backdrop-blur-sm rounded-full">
              <span class="relative flex h-2 w-2">
                <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-cyan-400 opacity-75"></span>
                <span class="relative inline-flex rounded-full h-2 w-2 bg-cyan-500"></span>
              </span>
              <span class="text-cyan-400/70 text-[10px] tracking-[0.2em] font-mono">SYSTEM ACTIVE</span>
              <span class="text-cyan-400/30 text-[10px]">v2.0.1</span>
            </div>
          </div>
  
          <div class="text-center mb-8">
            <h1 class="text-5xl md:text-7xl lg:text-8xl font-black tracking-tight">
              <span class="text-white/90 block mb-2 animate-slideUp">WELCOME TO</span>
              <span class="relative inline-block">
                <span class="absolute inset-0 bg-gradient-to-r from-cyan-400 via-blue-500 to-cyan-400 blur-2xl opacity-30 animate-pulseGlow"></span>
                <span class="relative bg-gradient-to-r from-cyan-400 via-teal-400 to-cyan-400 bg-clip-text text-transparent animate-gradient bg-[length:200%_auto]">
                  WATCH TOWER
                </span>
              </span>
            </h1>
          </div>
  
          <div class="flex justify-center items-center gap-4 mb-8">
            <div class="w-12 h-px bg-gradient-to-r from-transparent to-cyan-500/50"></div>
            <div class="w-1 h-1 bg-cyan-500/70 rotate-45"></div>
            <div class="w-12 h-px bg-gradient-to-l from-transparent to-cyan-500/50"></div>
          </div>
  
          <p class="text-center text-gray-400 text-sm md:text-base max-w-2xl mx-auto mb-12 font-light leading-relaxed">
            <span class="inline-block animate-fadeIn delay-100">Enterprise-grade real-time asset monitoring platform</span><br>
            <span class="inline-block animate-fadeIn delay-300">Built for security researchers and DevSecOps teams</span>
          </p>
  
          <div class="grid grid-cols-3 gap-6 md:gap-12 max-w-2xl mx-auto mb-16">
            <div class="text-center group">
              <div class="mb-2 flex justify-center">
                <svg class="w-6 h-6 text-cyan-500/40 group-hover:text-cyan-500/70 transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
              </div>
              <div class="text-white/80 text-2xl md:text-3xl font-bold mb-1">24/7</div>
              <div class="text-cyan-400/40 text-[10px] md:text-xs uppercase tracking-wider">Continuous Monitoring</div>
            </div>
            
            <div class="text-center group">
              <div class="mb-2 flex justify-center">
                <svg class="w-6 h-6 text-cyan-500/40 group-hover:text-cyan-500/70 transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"></path>
                </svg>
              </div>
              <div class="text-white/80 text-2xl md:text-3xl font-bold mb-1">99.99%</div>
              <div class="text-cyan-400/40 text-[10px] md:text-xs uppercase tracking-wider">Uptime SLA</div>
            </div>
            
            <div class="text-center group">
              <div class="mb-2 flex justify-center">
                <svg class="w-6 h-6 text-cyan-500/40 group-hover:text-cyan-500/70 transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
                </svg>
              </div>
              <div class="text-white/80 text-2xl md:text-3xl font-bold mb-1">Real-time</div>
              <div class="text-cyan-400/40 text-[10px] md:text-xs uppercase tracking-wider">WebSocket Alerts</div>
            </div>
          </div>
  
          <div class="flex flex-wrap justify-center gap-6 mb-12">
            <div class="flex items-center gap-2 text-xs text-gray-500">
              <svg class="w-3 h-3 text-cyan-500/50" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
              </svg>
              <span>Multi-Channel</span>
            </div>
            <div class="flex items-center gap-2 text-xs text-gray-500">
              <svg class="w-3 h-3 text-cyan-500/50" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
              </svg>
              <span>Laravel Echo</span>
            </div>
            <div class="flex items-center gap-2 text-xs text-gray-500">
              <svg class="w-3 h-3 text-cyan-500/50" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
              </svg>
              <span>SaaS Ready</span>
            </div>
          </div>
  
          <div class="flex flex-col sm:flex-row gap-5 justify-center">
            <button 
              @click="openGitHub"
              class="group relative px-10 py-3.5 bg-gradient-to-r from-cyan-500 to-blue-600 text-black text-sm uppercase tracking-wider font-bold overflow-hidden transition-all duration-300 hover:shadow-2xl hover:shadow-cyan-500/50 hover:scale-105"
            >
              <span class="relative z-10 flex items-center justify-center gap-2">
                <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
                  <path fill-rule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z" clip-rule="evenodd"></path>
                </svg>
                GitHub Repository
              </span>
              <div class="absolute inset-0 bg-gradient-to-r from-cyan-400 to-blue-400 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
            </button>
            
            <button 
              @click="showDevelopmentModal"
              class="group relative px-10 py-3.5 bg-transparent border border-cyan-500/40 text-cyan-400 text-sm uppercase tracking-wider font-medium overflow-hidden transition-all duration-300 hover:border-cyan-400 hover:shadow-lg hover:shadow-cyan-500/20 hover:scale-105"
            >
              <span class="relative z-10">Documentation</span>
              <div class="absolute inset-0 bg-cyan-500/10 scale-x-0 group-hover:scale-x-100 transition-transform duration-500 origin-left"></div>
            </button>
          </div>
  
          <div class="flex flex-wrap justify-center gap-3 mt-12">
            <span class="text-[10px] text-gray-600 px-2 py-1 border border-gray-800 rounded">Python 3</span>
            <span class="text-[10px] text-gray-600 px-2 py-1 border border-gray-800 rounded">Laravel 13</span>
            <span class="text-[10px] text-gray-600 px-2 py-1 border border-gray-800 rounded">Vue 3</span>
            <span class="text-[10px] text-gray-600 px-2 py-1 border border-gray-800 rounded">WebSocket</span>
            <span class="text-[10px] text-gray-600 px-2 py-1 border border-gray-800 rounded">TailwindCSS</span>
          </div>
  
          <div class="absolute bottom-8 left-8">
            <div class="w-20 h-px bg-gradient-to-r from-cyan-500/40 to-transparent"></div>
            <div class="w-px h-20 bg-gradient-to-b from-cyan-500/40 to-transparent mt-[-1px]"></div>
          </div>
          <div class="absolute bottom-8 right-8">
            <div class="w-20 h-px bg-gradient-to-l from-cyan-500/40 to-transparent"></div>
            <div class="w-px h-20 bg-gradient-to-t from-cyan-500/40 to-transparent mt-[-1px] ml-auto"></div>
          </div>
          <div class="absolute top-8 left-8">
            <div class="w-12 h-px bg-gradient-to-r from-cyan-500/20 to-transparent"></div>
          </div>
          <div class="absolute top-8 right-8">
            <div class="w-12 h-px bg-gradient-to-l from-cyan-500/20 to-transparent"></div>
          </div>
        </div>
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
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  
  const showModal = ref(false)
  
  const openGitHub = () => {
    window.open('https://github.com/AryaKhorasan/watch-tower', '_blank')
  }
  
  const showDevelopmentModal = () => {
    showModal.value = true
  }
  
  const closeModal = () => {
    showModal.value = false
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
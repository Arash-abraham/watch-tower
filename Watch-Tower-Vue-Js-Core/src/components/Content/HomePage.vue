<template>
  <div class="relative min-h-screen flex items-center justify-center">
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
          <span class="text-white/90 block mb-2">WELCOME TO</span>
          <span class="relative inline-block">
            <span class="absolute inset-0 bg-gradient-to-r from-cyan-400 via-blue-500 to-cyan-400 blur-2xl opacity-30"></span>
            <span class="relative bg-gradient-to-r from-cyan-400 via-teal-400 to-cyan-400 bg-clip-text text-transparent bg-[length:200%_auto] animate-gradient">
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
        <span class="inline-block">Enterprise-grade real-time asset monitoring platform</span><br>
        <span class="inline-block">Built for security researchers and DevSecOps teams</span>
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
</template>

<script setup>
const openGitHub = () => {
  window.open('https://github.com/AryaKhorasan/watch-tower', '_blank')
}

const showDevelopmentModal = () => {
  window.dispatchEvent(new CustomEvent('show-modal'))
}
</script>

<style scoped>
@keyframes gradient {
  0%, 100% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
}

.animate-gradient {
  background-size: 200% auto;
  animation: gradient 3s ease infinite;
}
</style>
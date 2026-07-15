<template>
    <div class="min-h-screen text-white pt-20 px-6">
      <div class="max-w-7xl mx-auto">
        <!-- Header -->
        <div class="mb-8">
          <div class="inline-flex items-center gap-3 px-4 py-2 border border-cyan-500/20 bg-cyan-500/5 backdrop-blur-sm rounded-full">
            <span class="relative flex h-2 w-2">
              <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-cyan-400 opacity-75"></span>
              <span class="relative inline-flex rounded-full h-2 w-2 bg-cyan-500"></span>
            </span>
            <span class="text-cyan-400/70 text-[10px] tracking-[0.2em] font-mono">MONITORS</span>
          </div>
        </div>
  
        <!-- Title -->
        <div class="mb-10">
          <h1 class="text-4xl md:text-5xl font-bold tracking-tight mb-2">
            <span class="text-white">Monitors</span>
          </h1>
          <p class="text-gray-500 text-sm">Configure and manage monitoring services</p>
        </div>
  
        <!-- Monitor Types -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-10">
          <div class="bg-gray-900/50 border border-cyan-500/10 rounded-xl p-6 hover:border-cyan-500/30 transition-all cursor-pointer">
            <div class="flex items-center justify-between mb-4">
              <div class="w-10 h-10 rounded-lg bg-cyan-500/10 border border-cyan-500/20 flex items-center justify-center">
                <svg class="w-5 h-5 text-cyan-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9"></path>
                </svg>
              </div>
              <span class="text-xs text-green-500/70 font-mono">ACTIVE</span>
            </div>
            <h3 class="text-lg font-semibold text-white mb-1">HTTP Monitor</h3>
            <p class="text-sm text-gray-500">Monitor HTTP/HTTPS endpoints</p>
            <div class="mt-4 flex items-center gap-4 text-xs text-gray-600">
              <span>2 targets</span>
              <span>•</span>
              <span>Avg: 124ms</span>
            </div>
          </div>
  
          <div class="bg-gray-900/50 border border-cyan-500/10 rounded-xl p-6 hover:border-cyan-500/30 transition-all cursor-pointer">
            <div class="flex items-center justify-between mb-4">
              <div class="w-10 h-10 rounded-lg bg-blue-500/10 border border-blue-500/20 flex items-center justify-center">
                <svg class="w-5 h-5 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M13 9l3 3m0 0l-3 3m3-3H8m13 0a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
              </div>
              <span class="text-xs text-green-500/70 font-mono">ACTIVE</span>
            </div>
            <h3 class="text-lg font-semibold text-white mb-1">Ping Monitor</h3>
            <p class="text-sm text-gray-500">ICMP ping monitoring</p>
            <div class="mt-4 flex items-center gap-4 text-xs text-gray-600">
              <span>4 targets</span>
              <span>•</span>
              <span>Avg: 12ms</span>
            </div>
          </div>
  
          <div class="bg-gray-900/50 border border-cyan-500/10 rounded-xl p-6 hover:border-cyan-500/30 transition-all cursor-pointer">
            <div class="flex items-center justify-between mb-4">
              <div class="w-10 h-10 rounded-lg bg-purple-500/10 border border-purple-500/20 flex items-center justify-center">
                <svg class="w-5 h-5 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 17V7m0 10a2 2 0 01-2 2H5a2 2 0 01-2-2V7a2 2 0 012-2h2a2 2 0 012 2m0 10a2 2 0 002 2h2a2 2 0 002-2M9 7a2 2 0 012-2h2a2 2 0 012 2m0 10V7m0 10a2 2 0 002 2h2a2 2 0 002-2V7a2 2 0 00-2-2h-2a2 2 0 00-2 2"></path>
                </svg>
              </div>
              <span class="text-xs text-yellow-500/70 font-mono">DEGRADED</span>
            </div>
            <h3 class="text-lg font-semibold text-white mb-1">Port Monitor</h3>
            <p class="text-sm text-gray-500">TCP port monitoring</p>
            <div class="mt-4 flex items-center gap-4 text-xs text-gray-600">
              <span>1 target</span>
              <span>•</span>
              <span>Avg: 45ms</span>
            </div>
          </div>
        </div>
  
        <!-- Active Monitors Table -->
        <div class="bg-gray-900/50 border border-gray-800 rounded-xl overflow-hidden">
          <div class="px-6 py-4 border-b border-gray-800">
            <h3 class="text-sm font-medium text-gray-300">Active Monitors</h3>
          </div>
          <div class="overflow-x-auto">
            <table class="w-full">
              <thead class="border-b border-gray-800">
                <tr>
                  <th class="text-left text-xs font-medium text-gray-500 uppercase tracking-wider px-6 py-4">Name</th>
                  <th class="text-left text-xs font-medium text-gray-500 uppercase tracking-wider px-6 py-4">Type</th>
                  <th class="text-left text-xs font-medium text-gray-500 uppercase tracking-wider px-6 py-4">Interval</th>
                  <th class="text-left text-xs font-medium text-gray-500 uppercase tracking-wider px-6 py-4">Status</th>
                  <th class="text-left text-xs font-medium text-gray-500 uppercase tracking-wider px-6 py-4">Uptime</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-gray-800">
                <tr v-for="monitor in monitors" :key="monitor.name" class="hover:bg-gray-800/30 transition-colors">
                  <td class="px-6 py-4 text-sm font-medium text-white">{{ monitor.name }}</td>
                  <td class="px-6 py-4 text-sm text-gray-400">{{ monitor.type }}</td>
                  <td class="px-6 py-4 text-sm text-gray-500 font-mono">{{ monitor.interval }}</td>
                  <td class="px-6 py-4">
                    <span class="inline-flex items-center gap-2 text-xs font-medium" :class="monitor.status === 'operational' ? 'text-green-500' : 'text-yellow-500'">
                      <span class="w-1.5 h-1.5 rounded-full" :class="monitor.status === 'operational' ? 'bg-green-500' : 'bg-yellow-500'"></span>
                      {{ monitor.status }}
                    </span>
                  </td>
                  <td class="px-6 py-4 text-sm text-green-400">{{ monitor.uptime }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  const monitors = [
    { name: 'Web Server Health', type: 'HTTP', interval: '30s', status: 'operational', uptime: '99.99%' },
    { name: 'Database Ping', type: 'Ping', interval: '60s', status: 'operational', uptime: '99.95%' },
    { name: 'API Gateway', type: 'HTTP', interval: '15s', status: 'operational', uptime: '99.98%' },
    { name: 'Redis Cache', type: 'Port', interval: '45s', status: 'degraded', uptime: '98.50%' },
  ]
  </script>
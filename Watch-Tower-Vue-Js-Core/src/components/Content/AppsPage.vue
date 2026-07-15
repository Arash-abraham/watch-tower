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
            <span class="text-cyan-400/70 text-[10px] tracking-[0.2em] font-mono">APPLICATIONS</span>
          </div>
        </div>
  
        <!-- Title -->
        <div class="mb-10">
          <h1 class="text-4xl md:text-5xl font-bold tracking-tight mb-2">
            <span class="text-white">Applications</span>
          </h1>
          <p class="text-gray-500 text-sm">Manage and monitor your applications</p>
        </div>
  
        <!-- Stats -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-10">
          <div class="bg-gray-900/50 border border-gray-800 rounded-xl p-4">
            <div class="text-gray-500 text-sm">Total Apps</div>
            <div class="text-2xl font-bold text-white mt-1">18</div>
          </div>
          <div class="bg-gray-900/50 border border-gray-800 rounded-xl p-4">
            <div class="text-gray-500 text-sm">Active</div>
            <div class="text-2xl font-bold text-green-500 mt-1">14</div>
          </div>
          <div class="bg-gray-900/50 border border-gray-800 rounded-xl p-4">
            <div class="text-gray-500 text-sm">Maintenance</div>
            <div class="text-2xl font-bold text-yellow-500 mt-1">4</div>
          </div>
        </div>
  
        <!-- App List -->
        <div class="bg-gray-900/50 border border-gray-800 rounded-xl overflow-hidden">
          <div class="overflow-x-auto">
            <table class="w-full">
              <thead class="border-b border-gray-800">
                <tr>
                  <th class="text-left text-xs font-medium text-gray-500 uppercase tracking-wider px-6 py-4">Application</th>
                  <th class="text-left text-xs font-medium text-gray-500 uppercase tracking-wider px-6 py-4">Status</th>
                  <th class="text-left text-xs font-medium text-gray-500 uppercase tracking-wider px-6 py-4">Type</th>
                  <th class="text-left text-xs font-medium text-gray-500 uppercase tracking-wider px-6 py-4">Last Check</th>
                  <th class="text-left text-xs font-medium text-gray-500 uppercase tracking-wider px-6 py-4">Response</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-gray-800">
                <tr v-for="app in apps" :key="app.name" class="hover:bg-gray-800/30 transition-colors">
                  <td class="px-6 py-4">
                    <div>
                      <div class="text-sm font-medium text-white">{{ app.name }}</div>
                      <div class="text-xs text-gray-500">{{ app.url }}</div>
                    </div>
                  </td>
                  <td class="px-6 py-4">
                    <span class="inline-flex items-center gap-2 text-xs font-medium" :class="app.status === 'online' ? 'text-green-500' : 'text-yellow-500'">
                      <span class="w-1.5 h-1.5 rounded-full" :class="app.status === 'online' ? 'bg-green-500' : 'bg-yellow-500'"></span>
                      {{ app.status === 'online' ? 'Online' : 'Degraded' }}
                    </span>
                  </td>
                  <td class="px-6 py-4 text-sm text-gray-400">{{ app.type }}</td>
                  <td class="px-6 py-4 text-sm text-gray-500">{{ app.lastCheck }}</td>
                  <td class="px-6 py-4">
                    <span class="text-sm font-mono" :class="app.response < 200 ? 'text-green-400' : 'text-yellow-400'">
                      {{ app.response }}ms
                    </span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  const apps = [
    { name: 'API Gateway', url: 'api.example.com', status: 'online', type: 'REST API', lastCheck: '2 min ago', response: 45 },
    { name: 'Web Dashboard', url: 'dashboard.example.com', status: 'online', type: 'Web App', lastCheck: '5 min ago', response: 120 },
    { name: 'Database', url: 'db.example.com', status: 'degraded', type: 'Database', lastCheck: '10 min ago', response: 350 },
    { name: 'Cache Service', url: 'cache.example.com', status: 'online', type: 'Redis', lastCheck: '15 min ago', response: 12 },
    { name: 'Queue Worker', url: 'queue.example.com', status: 'online', type: 'RabbitMQ', lastCheck: '20 min ago', response: 28 },
    { name: 'File Storage', url: 'storage.example.com', status: 'online', type: 'S3', lastCheck: '25 min ago', response: 89 },
  ]
  </script>
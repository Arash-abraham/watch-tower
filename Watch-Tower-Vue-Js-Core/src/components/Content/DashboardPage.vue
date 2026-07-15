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
            <span class="text-cyan-400/70 text-[10px] tracking-[0.2em] font-mono">DASHBOARD OVERVIEW</span>
            <span class="text-cyan-400/30 text-[10px]">v2.0.1</span>
          </div>
        </div>
  
        <!-- Title -->
        <div class="mb-10">
          <h1 class="text-4xl md:text-5xl font-bold tracking-tight mb-2">
            <span class="text-white">Dashboard</span>
          </h1>
          <p class="text-gray-500 text-sm">Real-time monitoring and system status overview</p>
        </div>
  
        <!-- Stats Grid -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-10">
          <div class="bg-gray-900/50 border border-gray-800 rounded-xl p-6 hover:border-cyan-500/30 transition-all">
            <div class="flex items-center justify-between mb-2">
              <span class="text-gray-500 text-sm font-medium">Total Monitors</span>
              <svg class="w-5 h-5 text-cyan-500/50" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 17V7m0 10a2 2 0 01-2 2H5a2 2 0 01-2-2V7a2 2 0 012-2h2a2 2 0 012 2m0 10a2 2 0 002 2h2a2 2 0 002-2M9 7a2 2 0 012-2h2a2 2 0 012 2m0 10V7m0 10a2 2 0 002 2h2a2 2 0 002-2V7a2 2 0 00-2-2h-2a2 2 0 00-2 2"></path>
              </svg>
            </div>
            <div class="text-3xl font-bold text-white">24</div>
            <div class="text-xs text-green-500 mt-1">+12% from last month</div>
          </div>
  
          <div class="bg-gray-900/50 border border-gray-800 rounded-xl p-6 hover:border-cyan-500/30 transition-all">
            <div class="flex items-center justify-between mb-2">
              <span class="text-gray-500 text-sm font-medium">Active Targets</span>
              <svg class="w-5 h-5 text-blue-500/50" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
              </svg>
            </div>
            <div class="text-3xl font-bold text-white">156</div>
            <div class="text-xs text-green-500 mt-1">+8% from last month</div>
          </div>
  
          <div class="bg-gray-900/50 border border-gray-800 rounded-xl p-6 hover:border-cyan-500/30 transition-all">
            <div class="flex items-center justify-between mb-2">
              <span class="text-gray-500 text-sm font-medium">Active Alerts</span>
              <svg class="w-5 h-5 text-yellow-500/50" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"></path>
              </svg>
            </div>
            <div class="text-3xl font-bold text-white">8</div>
            <div class="text-xs text-red-500 mt-1">+3 critical</div>
          </div>
  
          <div class="bg-gray-900/50 border border-gray-800 rounded-xl p-6 hover:border-cyan-500/30 transition-all">
            <div class="flex items-center justify-between mb-2">
              <span class="text-gray-500 text-sm font-medium">Uptime SLA</span>
              <svg class="w-5 h-5 text-green-500/50" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"></path>
              </svg>
            </div>
            <div class="text-3xl font-bold text-green-500">99.99%</div>
            <div class="text-xs text-gray-500 mt-1">Last 30 days</div>
          </div>
        </div>
  
        <!-- Charts Section -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-10">
          <div class="bg-gray-900/50 border border-gray-800 rounded-xl p-6">
            <div class="flex items-center justify-between mb-6">
              <h3 class="text-sm font-medium text-gray-300">System Performance</h3>
              <span class="text-xs text-cyan-500/70 font-mono">LIVE</span>
            </div>
            <div class="h-48 flex items-end justify-between gap-2">
              <div class="w-full flex items-end gap-1 h-40">
                <div v-for="i in 12" :key="i" 
                     class="flex-1 bg-gradient-to-t from-cyan-500/20 to-cyan-500/60 rounded-t"
                     :style="{ height: `${20 + Math.random() * 80}%` }">
                </div>
              </div>
            </div>
            <div class="flex justify-between mt-3 text-xs text-gray-600">
              <span>00:00</span>
              <span>06:00</span>
              <span>12:00</span>
              <span>18:00</span>
              <span>23:59</span>
            </div>
          </div>
  
          <div class="bg-gray-900/50 border border-gray-800 rounded-xl p-6">
            <div class="flex items-center justify-between mb-6">
              <h3 class="text-sm font-medium text-gray-300">Alert Distribution</h3>
              <span class="text-xs text-gray-600 font-mono">REAL-TIME</span>
            </div>
            <div class="space-y-4">
              <div>
                <div class="flex justify-between text-sm mb-1">
                  <span class="text-gray-400">Critical</span>
                  <span class="text-red-400 font-medium">3</span>
                </div>
                <div class="w-full bg-gray-800 rounded-full h-2">
                  <div class="bg-red-500 h-2 rounded-full" style="width: 37%"></div>
                </div>
              </div>
              <div>
                <div class="flex justify-between text-sm mb-1">
                  <span class="text-gray-400">Warning</span>
                  <span class="text-yellow-400 font-medium">5</span>
                </div>
                <div class="w-full bg-gray-800 rounded-full h-2">
                  <div class="bg-yellow-500 h-2 rounded-full" style="width: 63%"></div>
                </div>
              </div>
              <div>
                <div class="flex justify-between text-sm mb-1">
                  <span class="text-gray-400">Info</span>
                  <span class="text-blue-400 font-medium">12</span>
                </div>
                <div class="w-full bg-gray-800 rounded-full h-2">
                  <div class="bg-blue-500 h-2 rounded-full" style="width: 100%"></div>
                </div>
              </div>
            </div>
          </div>
        </div>
  
        <!-- Recent Activity -->
        <div class="bg-gray-900/50 border border-gray-800 rounded-xl p-6">
          <div class="flex items-center justify-between mb-6">
            <h3 class="text-sm font-medium text-gray-300">Recent Activity</h3>
            <button class="text-xs text-cyan-500 hover:text-cyan-400 transition-colors">View All</button>
          </div>
          <div class="space-y-3">
            <div class="flex items-center gap-4 p-3 border-b border-gray-800 hover:bg-gray-800/30 transition-colors rounded-lg">
              <div class="w-2 h-2 rounded-full bg-green-500"></div>
              <div class="flex-1">
                <p class="text-sm text-gray-300">Target <span class="text-cyan-400">api.example.com</span> is now online</p>
                <span class="text-xs text-gray-600">2 minutes ago</span>
              </div>
              <span class="text-xs text-green-500/70 font-mono">RECOVERED</span>
            </div>
            <div class="flex items-center gap-4 p-3 border-b border-gray-800 hover:bg-gray-800/30 transition-colors rounded-lg">
              <div class="w-2 h-2 rounded-full bg-red-500"></div>
              <div class="flex-1">
                <p class="text-sm text-gray-300">Critical alert: <span class="text-red-400">Database connection failed</span></p>
                <span class="text-xs text-gray-600">15 minutes ago</span>
              </div>
              <span class="text-xs text-red-500/70 font-mono">CRITICAL</span>
            </div>
            <div class="flex items-center gap-4 p-3 border-b border-gray-800 hover:bg-gray-800/30 transition-colors rounded-lg">
              <div class="w-2 h-2 rounded-full bg-yellow-500"></div>
              <div class="flex-1">
                <p class="text-sm text-gray-300">Monitor <span class="text-cyan-400">Ping Monitor #3</span> has high latency</p>
                <span class="text-xs text-gray-600">1 hour ago</span>
              </div>
              <span class="text-xs text-yellow-500/70 font-mono">WARNING</span>
            </div>
            <div class="flex items-center gap-4 p-3 hover:bg-gray-800/30 transition-colors rounded-lg">
              <div class="w-2 h-2 rounded-full bg-blue-500"></div>
              <div class="flex-1">
                <p class="text-sm text-gray-300">New target <span class="text-cyan-400">service.internal</span> added</p>
                <span class="text-xs text-gray-600">3 hours ago</span>
              </div>
              <span class="text-xs text-blue-500/70 font-mono">INFO</span>
            </div>
          </div>
        </div>
      </div>
    </div>
</template>
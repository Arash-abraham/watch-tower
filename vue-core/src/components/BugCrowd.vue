<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
    <!-- Notification Toast -->
    <div v-if="notification.show" class="fixed top-5 right-5 z-50 animate-fade-in">
      <div :class="[
        'px-4 py-3 rounded-xl shadow-lg backdrop-blur-md border',
        notification.type === 'success' 
          ? 'bg-emerald-500/20 border-emerald-500/50 text-emerald-400' 
          : 'bg-rose-500/20 border-rose-500/50 text-rose-400'
      ]">
        <div class="flex items-center gap-2">
          <svg v-if="notification.type === 'success'" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
          </svg>
          <svg v-else class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
          <span class="text-sm">{{ notification.message }}</span>
        </div>
      </div>
    </div>

    <!-- Header Section -->
    <header class="border-b border-slate-700/50 bg-slate-900/80 backdrop-blur-md sticky top-0 z-20">
      <div class="container mx-auto px-6 py-6">
        <div class="flex flex-col lg:flex-row justify-between items-center gap-5">
          <div class="flex items-center gap-4">
            <div class="w-12 h-12 bg-gradient-to-br from-red-500 to-orange-600 rounded-xl flex items-center justify-center shadow-lg shadow-red-500/25">
              <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="1.8">
                <path stroke-linecap="round" stroke-linejoin="round" d="M6.429 9.75L2.25 12l4.179 2.25m0-4.5l5.571 3 5.571-3m-11.142 0L2.25 7.5 12 2.25l9.75 5.25-4.179 2.25m0 0L21.75 12l-4.179 2.25m0 0l4.179 2.25L12 21.75 2.25 16.5l4.179-2.25m11.142 0l-5.571 3-5.571-3" />
              </svg>
            </div>
            <div>
              <h1 class="text-2xl font-bold tracking-tight bg-gradient-to-r from-white to-slate-400 bg-clip-text text-transparent">
                BugCrowd Intelligence
              </h1>
              <p class="text-xs text-slate-500 mt-0.5">Bug Bounty Program Dashboard</p>
            </div>
          </div>
          
          <div class="grid grid-cols-4 gap-3">
            <div class="px-4 py-2 bg-slate-800/40 rounded-xl border border-slate-700/30">
              <div class="text-xs text-slate-500 font-medium">PROGRAMS</div>
              <div class="text-2xl font-bold text-white">{{ filteredPrograms.length }}</div>
            </div>
            <div class="px-4 py-2 bg-slate-800/40 rounded-xl border border-slate-700/30">
              <div class="text-xs text-slate-500 font-medium">IN-SCOPE</div>
              <div class="text-2xl font-bold text-emerald-400">{{ totalInScope }}</div>
            </div>
            <div class="px-4 py-2 bg-slate-800/40 rounded-xl border border-slate-700/30">
              <div class="text-xs text-slate-500 font-medium">AVG PAYOUT</div>
              <div class="text-2xl font-bold text-amber-400">${{ avgPayout }}</div>
            </div>
            <div class="px-4 py-2 bg-slate-800/40 rounded-xl border border-slate-700/30">
              <div class="text-xs text-slate-500 font-medium">MAX BOUNTY</div>
              <div class="text-2xl font-bold text-rose-400">${{ maxPayout }}</div>
            </div>
          </div>
        </div>
        
        <div class="flex flex-col md:flex-row justify-between items-center gap-4 mt-6 pt-4 border-t border-slate-700/30">
          <div class="relative w-full md:w-96">
            <div class="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
              <svg class="w-4 h-4 text-slate-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
              </svg>
            </div>
            <input 
              v-model="searchQuery"
              type="text"
              placeholder="Search by program name or domain..."
              class="w-full pl-9 pr-4 py-2.5 bg-slate-800/40 border border-slate-700 rounded-xl focus:outline-none focus:border-rose-500 focus:ring-1 focus:ring-rose-500 text-white placeholder-slate-500 transition-all text-sm"
            >
          </div>
          
          <div class="flex items-center gap-3 w-full md:w-auto">
            <div class="flex bg-slate-800/40 rounded-xl p-1 border border-slate-700/30">
              <button 
                v-for="filter in filters" 
                :key="filter.value"
                @click="activeFilter = filter.value"
                :class="[
                  'px-4 py-1.5 text-sm font-medium rounded-lg transition-all',
                  activeFilter === filter.value 
                    ? 'bg-rose-500 text-white shadow-md' 
                    : 'text-slate-400 hover:text-white hover:bg-slate-700/50'
                ]"
              >
                {{ filter.label }}
              </button>
            </div>
            
            <button 
              @click="sortOrder = sortOrder === 'desc' ? 'asc' : 'desc'"
              class="flex items-center gap-2 px-3 py-2.5 bg-slate-800/40 border border-slate-700 rounded-xl hover:border-slate-500 transition-all text-sm text-slate-300"
            >
              <span>Payout</span>
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path v-if="sortOrder === 'desc'" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4h13M3 8h9m-9 4h6m4 0l4-4m0 0l4 4m-4-4v12" />
                <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4h13M3 8h9m-9 4h6m4 8l4-4m0 0l-4-4m4 4H3" />
              </svg>
            </button>
            
            <div class="flex bg-slate-800/40 rounded-xl p-1 border border-slate-700/30">
              <button 
                @click="viewMode = 'grid'"
                :class="[
                  'p-1.5 rounded-lg transition-all',
                  viewMode === 'grid' ? 'bg-rose-500 text-white' : 'text-slate-400 hover:text-white'
                ]"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z" />
                </svg>
              </button>
              <button 
                @click="viewMode = 'list'"
                :class="[
                  'p-1.5 rounded-lg transition-all',
                  viewMode === 'list' ? 'bg-rose-500 text-white' : 'text-slate-400 hover:text-white'
                ]"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
                </svg>
              </button>
            </div>
          </div>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="container mx-auto px-6 py-8">
      <!-- Grid View -->
      <div v-if="viewMode === 'grid'" class="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
        <div 
          v-for="program in paginatedPrograms" 
          :key="program.name"
          class="group bg-slate-800/30 backdrop-blur-sm rounded-xl border border-slate-700/40 hover:border-rose-500/40 transition-all duration-300 hover:transform hover:-translate-y-1 hover:shadow-xl hover:shadow-rose-500/5"
        >
          <div class="p-5 border-b border-slate-700/30">
            <div class="flex justify-between items-start gap-3">
              <div class="flex-1 min-w-0">
                <h2 class="text-lg font-semibold text-white leading-tight line-clamp-2">
                  {{ program.name }}
                </h2>
                <div class="flex items-center gap-2 mt-2">
                  <span class="inline-flex items-center text-xs px-2 py-0.5 bg-amber-500/10 text-amber-400 rounded-full font-medium">
                    <span class="w-1 h-1 bg-amber-400 rounded-full mr-1.5"></span>
                    ${{ program.max_payout.toLocaleString() }}
                  </span>
                  <span v-if="program.managed_by_bugcrowd === 'true'" class="text-xs px-2 py-0.5 bg-blue-500/10 text-blue-400 rounded-full font-medium">
                    BugCrowd Managed
                  </span>
                </div>
              </div>
              <div class="flex flex-col items-end">
                <div class="text-right">
                  <div class="text-2xl font-bold text-white">${{ program.max_payout.toLocaleString() }}</div>
                  <div class="text-[10px] text-slate-500 uppercase tracking-wider mt-0.5">Max Bounty</div>
                </div>
              </div>
            </div>
            
            <div class="flex flex-wrap gap-2 mt-4">
              <span class="text-xs px-2 py-1 bg-emerald-500/10 text-emerald-400 rounded-md flex items-center gap-1">
                <span class="w-1.5 h-1.5 bg-emerald-400 rounded-full"></span>
                In-Scope: {{ program.targets.in_scope.length }}
              </span>
              <span class="text-xs px-2 py-1 bg-rose-500/10 text-rose-400 rounded-md flex items-center gap-1">
                <span class="w-1.5 h-1.5 bg-rose-400 rounded-full"></span>
                Out: {{ program.targets.out_of_scope.length }}
              </span>
              <span v-if="program.allows_disclosure === 'true'" class="text-xs px-2 py-1 bg-purple-500/10 text-purple-400 rounded-md">
                Disclosure Allowed
              </span>
              <span v-if="program.safe_harbor === 'full'" class="text-xs px-2 py-1 bg-green-500/10 text-green-400 rounded-md">
                Full Safe Harbor
              </span>
            </div>
          </div>

          <div class="px-5 pt-4">
            <div class="flex justify-between items-center text-xs mb-1.5">
              <span class="text-slate-500">Scope Coverage</span>
              <span class="text-slate-300 font-mono">{{ scopeCoverage(program) }}%</span>
            </div>
            <div class="w-full bg-slate-700/50 rounded-full h-1.5 overflow-hidden">
              <div 
                class="bg-gradient-to-r from-emerald-500 to-teal-500 h-1.5 rounded-full transition-all duration-500"
                :style="{ width: scopeCoverage(program) + '%' }"
              ></div>
            </div>
          </div>

          <div class="p-5 pb-3">
            <div class="flex items-center justify-between mb-3">
              <div class="flex items-center gap-2">
                <div class="w-1.5 h-1.5 bg-emerald-500 rounded-full"></div>
                <h3 class="text-xs font-semibold text-slate-400 uppercase tracking-wider">In-Scope Targets</h3>
              </div>
              <span class="text-[11px] text-slate-500">{{ program.targets.in_scope.length }} assets</span>
            </div>
            <div class="space-y-2 max-h-44 overflow-y-auto custom-scrollbar pr-1">
              <div 
                v-for="target in program.targets.in_scope.slice(0, 6)" 
                :key="target.target"
                class="flex items-center justify-between p-2 bg-slate-900/30 rounded-lg hover:bg-slate-900/50 transition-colors group/target"
              >
                <div class="flex items-center gap-2 flex-1 min-w-0">
                  <div class="w-1 h-1 bg-emerald-500 rounded-full flex-shrink-0"></div>
                  <div class="text-sm text-slate-300 truncate font-mono">{{ target.target }}</div>
                </div>
                <div class="flex items-center gap-2 flex-shrink-0">
                  <span class="text-[10px] px-1.5 py-0.5 bg-slate-800 rounded text-slate-400 font-mono uppercase">
                    {{ target.type || 'web' }}
                  </span>
                  <button 
                    @click="copyToClipboard(target.target)"
                    class="opacity-0 group-hover/target:opacity-100 transition-opacity p-1 hover:bg-slate-700 rounded"
                    title="Copy URL"
                  >
                    <svg class="w-3 h-3 text-slate-500 hover:text-slate-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"/>
                    </svg>
                  </button>
                </div>
              </div>
              <div v-if="program.targets.in_scope.length > 6" class="text-center text-xs text-slate-500 pt-1">
                +{{ program.targets.in_scope.length - 6 }} additional targets
              </div>
              <div v-if="program.targets.in_scope.length === 0" class="text-center text-sm text-slate-600 py-3 italic">
                No targets in scope
              </div>
            </div>
          </div>

          <!-- Out of Scope Section - FIXED -->
          <div class="px-5 pb-2" v-if="program.targets.out_of_scope.length > 0">
            <button 
              @click="toggleOutOfScope(program.name)"
              class="flex items-center justify-between w-full text-xs font-medium text-slate-500 hover:text-slate-300 transition-colors py-1"
            >
              <span>Out-of-Scope ({{ program.targets.out_of_scope.length }})</span>
              <svg class="w-3.5 h-3.5 transition-transform duration-200" :class="{ 'rotate-180': expandedOutOfScope[program.name] }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
              </svg>
            </button>
            <div v-show="expandedOutOfScope[program.name]" class="mt-2 space-y-1 max-h-28 overflow-y-auto custom-scrollbar">
              <div 
                v-for="target in program.targets.out_of_scope" 
                :key="target.target"
                class="flex items-center gap-2 text-xs p-1.5 text-slate-500 font-mono"
              >
                <div class="w-1 h-1 bg-rose-500/50 rounded-full flex-shrink-0"></div>
                <span class="truncate">{{ target.target }}</span>
              </div>
            </div>
          </div>

          <div class="p-5 pt-4 border-t border-slate-700/30 flex justify-between items-center">
            <div class="flex items-center gap-2 text-[11px] text-slate-500">
              <div class="flex items-center gap-1">
                <div class="w-3 h-3 rounded-sm bg-emerald-500/20 flex items-center justify-center">
                  <div class="w-1 h-1 bg-emerald-500 rounded-full"></div>
                </div>
                <span>API: {{ countType(program.targets.in_scope, 'api') }}</span>
              </div>
              <div class="flex items-center gap-1">
                <div class="w-3 h-3 rounded-sm bg-blue-500/20 flex items-center justify-center">
                  <div class="w-1 h-1 bg-blue-500 rounded-full"></div>
                </div>
                <span>Web: {{ countType(program.targets.in_scope, 'website') }}</span>
              </div>
            </div>
            <div class="flex items-center gap-2">
              <div class="relative">
                <button 
                  @click="toggleShareMenu(program.name)"
                  class="p-1.5 rounded-lg hover:bg-slate-700/50 transition-colors"
                  title="Share Program"
                >
                  <svg class="w-4 h-4 text-slate-500 hover:text-slate-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.368 2.684 3 3 0 00-5.368-2.684z"/>
                  </svg>
                </button>
                <div v-if="activeShareMenu === program.name" class="absolute bottom-full right-0 mb-2 bg-slate-800 border border-slate-700 rounded-xl shadow-xl z-30 min-w-[140px]">
                  <div class="py-1">
                    <button @click="shareOnX(program)" class="flex items-center gap-3 px-4 py-2 text-sm text-white hover:bg-slate-700 w-full text-left">
                      <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>
                      X (Twitter)
                    </button>
                    <button @click="shareOnTelegram(program)" class="flex items-center gap-3 px-4 py-2 text-sm text-white hover:bg-slate-700 w-full text-left">
                      <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24"><path d="M12 0C5.373 0 0 5.373 0 12s5.373 12 12 12 12-5.373 12-12S18.627 0 12 0zm5.562 8.161c-.18 1.897-.962 6.502-1.359 8.627-.168.9-.5 1.201-.82 1.23-.697.065-1.226-.461-1.901-.904-1.056-.692-1.653-1.123-2.678-1.799-1.185-.78-.417-1.21.258-1.91.176-.184 3.246-2.975 3.307-3.23.007-.032.014-.15-.056-.212-.07-.063-.173-.041-.247-.024-.105.024-1.793 1.14-5.061 3.345-.48.33-.914.49-1.302.48-.428-.01-1.252-.242-1.864-.441-.75-.244-1.346-.373-1.294-.788.027-.216.325-.437.893-.663 3.498-1.524 5.83-2.529 6.998-3.014 3.332-1.386 4.025-1.627 4.476-1.635.099-.002.32.023.463.139.121.099.153.232.168.327.015.095.034.311.02.48z"/></svg>
                      Telegram
                    </button>
                    <button @click="shareOnLinkedIn(program)" class="flex items-center gap-3 px-4 py-2 text-sm text-white hover:bg-slate-700 w-full text-left">
                      <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451c.979 0 1.771-.773 1.771-1.729V1.729C24 .774 23.203 0 22.225 0z"/></svg>
                      LinkedIn
                    </button>
                  </div>
                </div>
              </div>
              <a 
                :href="program.url" 
                target="_blank"
                class="text-sm px-4 py-1.5 bg-gradient-to-r from-rose-500 to-rose-600 hover:from-rose-600 hover:to-rose-700 rounded-lg transition-all duration-200 shadow-md hover:shadow-rose-500/20"
              >
                View on BugCrowd
              </a>
            </div>
          </div>
        </div>
      </div>

      <!-- List View -->
      <div v-else class="space-y-3">
        <div 
          v-for="program in paginatedPrograms" 
          :key="program.name"
          class="group bg-slate-800/30 backdrop-blur-sm rounded-xl border border-slate-700/40 hover:border-rose-500/30 transition-all p-4"
        >
          <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
            <div class="flex-1 min-w-0">
              <div class="flex items-center gap-3 flex-wrap">
                <h3 class="text-base font-semibold text-white">{{ program.name }}</h3>
                <span class="text-xs px-2 py-0.5 bg-amber-500/10 text-amber-400 rounded-full font-mono">
                  ${{ program.max_payout.toLocaleString() }}
                </span>
                <span v-if="program.managed_by_bugcrowd === 'true'" class="text-xs px-2 py-0.5 bg-blue-500/10 text-blue-400 rounded-full">
                  Managed
                </span>
              </div>
              <div class="flex flex-wrap gap-x-6 gap-y-1 mt-2 text-xs text-slate-500">
                <span>In-Scope: {{ program.targets.in_scope.length }}</span>
                <span>Out-of-Scope: {{ program.targets.out_of_scope.length }}</span>
                <span v-if="program.allows_disclosure === 'true'">Disclosure Allowed</span>
                <span class="font-mono">{{ program.safe_harbor || 'Full Safe Harbor' }}</span>
              </div>
              <div class="flex flex-wrap gap-2 mt-2">
                <span 
                  v-for="target in program.targets.in_scope.slice(0, 3)" 
                  :key="target.target"
                  class="text-xs text-slate-400 bg-slate-800/50 px-2 py-0.5 rounded font-mono"
                >
                  {{ target.target }}
                </span>
                <span v-if="program.targets.in_scope.length > 3" class="text-xs text-slate-500">
                  +{{ program.targets.in_scope.length - 3 }}
                </span>
              </div>
            </div>
            <div class="flex items-center gap-2">
              <div class="relative">
                <button 
                  @click="toggleShareMenu(program.name)"
                  class="p-2 rounded-lg hover:bg-slate-700/50 transition-colors"
                  title="Share"
                >
                  <svg class="w-4 h-4 text-slate-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.368 2.684 3 3 0 00-5.368-2.684z"/>
                  </svg>
                </button>
                <div v-if="activeShareMenu === program.name" class="absolute bottom-full right-0 mb-2 bg-slate-800 border border-slate-700 rounded-xl shadow-xl z-30 min-w-[140px]">
                  <div class="py-1">
                    <button @click="shareOnX(program)" class="flex items-center gap-3 px-4 py-2 text-sm text-white hover:bg-slate-700 w-full text-left">X (Twitter)</button>
                    <button @click="shareOnTelegram(program)" class="flex items-center gap-3 px-4 py-2 text-sm text-white hover:bg-slate-700 w-full text-left">Telegram</button>
                    <button @click="shareOnLinkedIn(program)" class="flex items-center gap-3 px-4 py-2 text-sm text-white hover:bg-slate-700 w-full text-left">LinkedIn</button>
                  </div>
                </div>
              </div>
              <button 
                @click="copyToClipboard(program.url)"
                class="p-2 rounded-lg hover:bg-slate-700/50 transition-colors"
                title="Copy URL"
              >
                <svg class="w-4 h-4 text-slate-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"/>
                </svg>
              </button>
              <a 
                :href="program.url" 
                target="_blank"
                class="text-sm px-4 py-1.5 bg-rose-500/20 text-rose-400 hover:bg-rose-500/30 rounded-lg transition-all"
              >
                View Program
              </a>
            </div>
          </div>
        </div>
      </div>

      <!-- Pagination -->
      <div v-if="filteredPrograms.length > 0" class="flex justify-center items-center gap-3 mt-10 pt-4 border-t border-slate-700/30">
        <button 
          @click="currentPage--"
          :disabled="currentPage === 1"
          :class="[
            'p-2 rounded-lg transition-all',
            currentPage === 1 ? 'text-slate-600 cursor-not-allowed' : 'text-slate-400 hover:text-white hover:bg-slate-800'
          ]"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
          </svg>
        </button>
        <div class="flex gap-1">
          <button 
            v-for="page in totalPages"
            :key="page"
            @click="currentPage = page"
            :class="[
              'w-8 h-8 text-sm rounded-lg transition-all',
              currentPage === page 
                ? 'bg-rose-500 text-white shadow-md' 
                : 'text-slate-400 hover:text-white hover:bg-slate-800'
            ]"
          >
            {{ page }}
          </button>
        </div>
        <button 
          @click="currentPage++"
          :disabled="currentPage === totalPages"
          :class="[
            'p-2 rounded-lg transition-all',
            currentPage === totalPages ? 'text-slate-600 cursor-not-allowed' : 'text-slate-400 hover:text-white hover:bg-slate-800'
          ]"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
          </svg>
        </button>
      </div>

      <!-- Empty State -->
      <div v-if="filteredPrograms.length === 0" class="text-center py-16">
        <div class="w-24 h-24 mx-auto mb-6 bg-slate-800/50 rounded-2xl flex items-center justify-center">
          <svg class="w-12 h-12 text-slate-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
          </svg>
        </div>
        <h3 class="text-xl font-semibold text-slate-400 mb-2">No programs found</h3>
        <p class="text-slate-500 text-sm">Try adjusting your search or filter criteria</p>
        <button 
          @click="searchQuery = ''; activeFilter = 'all'"
          class="mt-6 px-5 py-2 bg-slate-800 hover:bg-slate-700 rounded-xl transition-colors text-sm"
        >
          Clear all filters
        </button>
      </div>
    </main>
  </div>
</template>

<script>
export default {
  name: 'BugCrowd',
  data() {
    return {
      searchQuery: '',
      activeFilter: 'all',
      sortOrder: 'desc',
      viewMode: 'grid',
      currentPage: 1,
      itemsPerPage: 9,
      expandedOutOfScope: {},
      activeShareMenu: null,
      notification: {
        show: false,
        message: '',
        type: 'success'
      },
      filters: [
        { label: 'All Programs', value: 'all' },
        { label: 'High Bounty (+$10k)', value: 'high' },
        { label: 'Managed by BC', value: 'managed' },
        { label: 'Disclosure Allowed', value: 'disclosure' }
      ],
      programs: [
        {
          "name": "CoinDesk Data - Data API",
          "url": "https://bugcrowd.com/engagements/CCData-mbb-og",
          "allows_disclosure": "false",
          "managed_by_bugcrowd": "true",
          "safe_harbor": "full",
          "max_payout": 7500,
          "targets": {
            "in_scope": [
              { "type": "api", "target": "http://data-api.coindesk.com/", "name": "CoinDesk Data - Data API" },
              { "type": "api", "target": "https://tools-api.cryptocompare.com/", "name": "CoinDesk Data - Tools API" }
            ],
            "out_of_scope": [
              { "type": "website", "target": "https://www.coindesk.com/", "name": "coindesk.com" },
              { "type": "website", "target": "https://uat.coindesk.com/", "name": "uat.coindesk.com" },
              { "type": "website", "target": "https://events.coindesk.com", "name": "Production CoinDesk Events" }
            ]
          }
        },
        {
          "name": "Acorns Grow, Inc.",
          "url": "https://bugcrowd.com/engagements/acorns",
          "allows_disclosure": "true",
          "managed_by_bugcrowd": "true",
          "safe_harbor": "full",
          "max_payout": 4000,
          "targets": {
            "in_scope": [
              { "type": "website", "target": "https://acorns.com/", "name": "acorns.com" },
              { "type": "api", "target": "https://api.acorns.com/", "name": "Acorns API" }
            ],
            "out_of_scope": [
              { "type": "website", "target": "https://help.acorns.com/", "name": "help.acorns.com" }
            ]
          }
        },
        {
          "name": "Tesla, Inc.",
          "url": "https://bugcrowd.com/engagements/tesla",
          "allows_disclosure": "true",
          "managed_by_bugcrowd": "false",
          "safe_harbor": "full",
          "max_payout": 15000,
          "targets": {
            "in_scope": [
              { "type": "website", "target": "https://www.tesla.com/", "name": "tesla.com" },
              { "type": "api", "target": "https://owner-api.teslamotors.com/", "name": "Tesla Owner API" }
            ],
            "out_of_scope": [
              { "type": "website", "target": "https://shop.tesla.com/", "name": "shop.tesla.com" }
            ]
          }
        },
        {
          "name": "Microsoft Corporation",
          "url": "https://bugcrowd.com/microsoft",
          "allows_disclosure": "true",
          "managed_by_bugcrowd": "false",
          "safe_harbor": "full",
          "max_payout": 20000,
          "targets": {
            "in_scope": [
              { "type": "website", "target": "https://*.microsoft.com/", "name": "microsoft.com" },
              { "type": "api", "target": "https://api.microsoft.com/", "name": "Microsoft API" }
            ],
            "out_of_scope": [
              { "type": "website", "target": "https://support.microsoft.com/", "name": "support.microsoft.com" }
            ]
          }
        }
      ]
    }
  },
  computed: {
    filteredPrograms() {
      let result = this.programs
      
      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase()
        result = result.filter(p => 
          p.name.toLowerCase().includes(query) ||
          p.targets.in_scope.some(t => t.target.toLowerCase().includes(query))
        )
      }
      
      if (this.activeFilter === 'high') {
        result = result.filter(p => p.max_payout >= 10000)
      } else if (this.activeFilter === 'managed') {
        result = result.filter(p => p.managed_by_bugcrowd === 'true')
      } else if (this.activeFilter === 'disclosure') {
        result = result.filter(p => p.allows_disclosure === 'true')
      }
      
      if (this.sortOrder === 'desc') {
        result = [...result].sort((a, b) => b.max_payout - a.max_payout)
      } else {
        result = [...result].sort((a, b) => a.max_payout - b.max_payout)
      }
      
      return result
    },
    paginatedPrograms() {
      const start = (this.currentPage - 1) * this.itemsPerPage
      return this.filteredPrograms.slice(start, start + this.itemsPerPage)
    },
    totalPages() {
      return Math.ceil(this.filteredPrograms.length / this.itemsPerPage)
    },
    totalInScope() {
      return this.programs.reduce((sum, p) => sum + p.targets.in_scope.length, 0)
    },
    avgPayout() {
      const avg = this.programs.reduce((sum, p) => sum + p.max_payout, 0) / this.programs.length
      return Math.round(avg).toLocaleString()
    },
    maxPayout() {
      return Math.max(...this.programs.map(p => p.max_payout)).toLocaleString()
    }
  },
  methods: {
    showNotification(message, type = 'success') {
      this.notification = { show: true, message, type }
      setTimeout(() => {
        this.notification.show = false
      }, 2000)
    },
    scopeCoverage(program) {
      const total = program.targets.in_scope.length + program.targets.out_of_scope.length
      if (total === 0) return 0
      return Math.round((program.targets.in_scope.length / total) * 100)
    },
    countType(targets, type) {
      return targets.filter(t => t.type === type).length
    },
    toggleOutOfScope(programName) {
      this.expandedOutOfScope[programName] = !this.expandedOutOfScope[programName]
    },
    toggleShareMenu(programName) {
      if (this.activeShareMenu === programName) {
        this.activeShareMenu = null
      } else {
        this.activeShareMenu = programName
      }
    },
    copyToClipboard(text) {
      navigator.clipboard.writeText(text)
      this.showNotification('Copied to clipboard!')
    },
    shareOnX(program) {
      const text = encodeURIComponent(`${program.name} - Bug Bounty Program with max payout $${program.max_payout}`)
      window.open(`https://twitter.com/intent/tweet?text=${text}&url=${encodeURIComponent(program.url)}`, '_blank')
      this.activeShareMenu = null
    },
    shareOnTelegram(program) {
      window.open(`https://t.me/share/url?url=${encodeURIComponent(program.url)}&text=${encodeURIComponent(`${program.name} - $${program.max_payout} max payout`)}`, '_blank')
      this.activeShareMenu = null
    },
    shareOnLinkedIn(program) {
      window.open(`https://www.linkedin.com/sharing/share-offsite/?url=${encodeURIComponent(program.url)}`, '_blank')
      this.activeShareMenu = null
    }
  },
  watch: {
    searchQuery() {
      this.currentPage = 1
    },
    activeFilter() {
      this.currentPage = 1
    }
  },
  mounted() {
    this.programs.forEach(program => {
      this.expandedOutOfScope[program.name] = false
    })
  }
}
</script>

<style scoped>
@keyframes fade-in {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
.animate-fade-in {
  animation: fade-in 0.2s ease-out;
}
.custom-scrollbar::-webkit-scrollbar {
  width: 4px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  background: rgba(51, 65, 85, 0.3);
  border-radius: 10px;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background: rgba(239, 68, 68, 0.4);
  border-radius: 10px;
}
.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: rgba(239, 68, 68, 0.6);
}
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>

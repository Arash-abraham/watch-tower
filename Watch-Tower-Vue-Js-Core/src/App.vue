<template>
  <div class="relative flex min-h-screen flex-col">
    <!-- ══════════════ Global backdrop (never intercepts clicks) ══════════════ -->
    <div class="pointer-events-none absolute inset-0 z-0 overflow-hidden" aria-hidden="true">
      <!-- vertical gradient wash -->
      <div class="absolute inset-0 bg-gradient-to-b from-cyan-500/[0.05] via-transparent to-blue-600/[0.06]"></div>

      <!-- blueprint grid (correct arbitrary background-size syntax) -->
      <div class="absolute inset-0 bg-grid opacity-60"></div>

      <!-- soft ambient glows -->
      <div class="absolute -left-40 top-10 h-96 w-96 rounded-full bg-cyan-500/10 blur-[120px] animate-glow-pulse"></div>
      <div class="absolute -right-32 top-1/3 h-96 w-96 rounded-full bg-blue-600/10 blur-[130px] animate-glow-pulse [animation-delay:2s]"></div>
      <div class="absolute bottom-0 left-1/3 h-80 w-80 rounded-full bg-teal-500/[0.07] blur-[120px]"></div>

      <!-- scan sweeps -->
      <div class="absolute left-0 top-0 h-px w-full bg-gradient-to-r from-transparent via-cyan-400/40 to-transparent animate-scan-x"></div>
      <div class="absolute left-0 top-0 h-full w-px bg-gradient-to-b from-transparent via-cyan-400/25 to-transparent animate-scan-y"></div>

      <!-- floating dust -->
      <div class="absolute left-[12%] top-[22%] h-1 w-1 rounded-full bg-cyan-300/60 animate-float-y"></div>
      <div class="absolute left-[82%] top-[58%] h-1.5 w-1.5 rounded-full bg-blue-300/40 animate-float-y [animation-delay:1.5s]"></div>
      <div class="absolute left-[26%] top-[78%] h-1 w-1 rounded-full bg-cyan-300/50 animate-float-y [animation-delay:3s]"></div>
      <div class="absolute left-[68%] top-[36%] h-1 w-1 rounded-full bg-white/30 animate-float-y [animation-delay:4.5s]"></div>

      <!-- vignette -->
      <div class="absolute inset-0 bg-[radial-gradient(ellipse_at_center,transparent_35%,rgba(2,4,7,0.75)_100%)]"></div>
    </div>

    <Navbar />

    <!-- ══════════════ Page content (above the backdrop) ══════════════ -->
    <main class="relative z-10 flex-1">
      <router-view v-slot="{ Component }">
        <transition name="page" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>

    <Footer class="relative z-10" />

    <!-- ══════════════ "Under development" dialog ══════════════ -->
    <Teleport to="body">
      <transition name="modal">
        <div
          v-if="showModal"
          class="fixed inset-0 z-[100] flex items-center justify-center px-4 py-10"
          role="dialog"
          aria-modal="true"
          aria-labelledby="dev-modal-title"
          @click.self="closeModal"
        >
          <div class="absolute inset-0 bg-black/80 backdrop-blur-md"></div>

          <div class="relative w-full max-w-md animate-modal-in">
            <div class="absolute -inset-px rounded-2xl bg-gradient-to-br from-cyan-400/60 via-blue-500/20 to-transparent blur-[2px]"></div>

            <div class="relative rounded-2xl border border-white/10 bg-gradient-to-br from-[#0a1219] to-[#04070a] p-8 shadow-glow">
              <button
                class="absolute right-4 top-4 grid h-8 w-8 place-items-center rounded-lg text-gray-500 transition-colors hover:bg-white/5 hover:text-gray-200"
                aria-label="Close dialog"
                @click="closeModal"
              >
                <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>

              <div class="mb-6 flex justify-center">
                <div class="grid h-16 w-16 place-items-center rounded-full border border-cyan-400/30 bg-gradient-to-br from-cyan-400/20 to-blue-600/20">
                  <svg class="h-8 w-8 text-cyan-300" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="1.5">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M13 10V3L4 14h7v7l9-11h-7z" />
                  </svg>
                </div>
              </div>

              <h3 id="dev-modal-title" class="mb-3 text-center text-2xl font-bold text-white">Under Development</h3>
              <div class="divider mx-auto mb-4 w-24"></div>

              <p class="mb-6 text-center text-sm leading-relaxed text-gray-400">
                This feature is currently in active development.<br />
                Our team is working hard to deliver an exceptional experience.
              </p>

              <div class="mb-6 flex justify-center">
                <span class="chip">Coming soon</span>
              </div>

              <div class="mb-6 h-1 w-full overflow-hidden rounded-full bg-white/10">
                <div class="h-1 rounded-full bg-gradient-to-r from-cyan-400 to-blue-500 animate-progress-bar"></div>
              </div>

              <button class="btn-ghost w-full" @click="closeModal">Got it</button>
            </div>
          </div>
        </div>
      </transition>
    </Teleport>
  </div>
</template>

<script setup>
import { onMounted, onUnmounted, ref } from 'vue'
import Navbar from './components/layouts/partials/Navbar.vue'
import Footer from './components/layouts/partials/Footer.vue'

const showModal = ref(false)

function openModal() {
  showModal.value = true
}

function closeModal() {
  showModal.value = false
}

function onKeydown(event) {
  if (event.key === 'Escape' && showModal.value) closeModal()
}

// Both a global helper and a DOM event are supported so any page can open
// the "under development" dialog.
window.showDevelopmentModal = openModal

onMounted(() => {
  window.addEventListener('show-modal', openModal)
  window.addEventListener('keydown', onKeydown)
})

onUnmounted(() => {
  window.removeEventListener('show-modal', openModal)
  window.removeEventListener('keydown', onKeydown)
  delete window.showDevelopmentModal
})
</script>

<style>
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.2s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}
</style>

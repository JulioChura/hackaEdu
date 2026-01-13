<template>
  <section class="py-16 sm:py-24 bg-white relative">
    <div class="max-w-7xl mx-auto px-4 sm:px-6">
      <!-- Header -->
      <div class="mb-12 sm:mb-16 max-w-2xl">
        <h2 class="text-3xl sm:text-4xl font-bold text-charcoal mb-3 sm:mb-4">How it works</h2>
        <p class="text-base sm:text-lg text-slate-text leading-relaxed">
          Our AI-driven process simplifies your path to reading mastery in three simple steps.
        </p>
      </div>
      
      <!-- Cards Grid -->
      <div class="grid sm:grid-cols-2 md:grid-cols-3 gap-6 sm:gap-8">
        <CardHome 
          icon="psychology"
          title="1. AI Generation"
          description="Instantly create unique texts based on your interests. The engine adapts vocabulary and grammar to match your exact level."
        />
        
        <CardHome 
          icon="menu_book"
          title="2. Interactive Reading"
          description="Read with confidence. Click any word for instant definitions, translations, and grammatical context without leaving the page."
        />
        
        <CardHome 
          icon="monitoring"
          title="3. Track Mastery"
          description="Visualize your vocabulary growth over time. Our analytics dashboard shows exactly which CEFR levels you are mastering."
        />
      </div>
    </div>
  </section>
</template>

<script setup>
import CardHome from './CardHome.vue'
</script>

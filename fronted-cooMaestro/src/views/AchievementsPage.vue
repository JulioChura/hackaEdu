<script setup>
import { ref } from 'vue'
import AchievementsHeader from '@/components/achievements/AchievementsHeader.vue'
import AchievementCard from '@/components/achievements/AchievementCard.vue'

// Mock data - TODO: Replace with API call
const achievements = ref([
  {
    id: 1,
    emoji: '🎯',
    title: 'First Step',
    unlocked: true,
    achievedDate: 'Achieved Oct 12, 2023',
    description: "Bravo! You've successfully completed your first module and joined the community."
  },
  {
    id: 2,
    emoji: '📚',
    title: 'Dedicated Student',
    unlocked: true,
    achievedDate: 'Achieved Nov 05, 2023',
    description: "Consistency is key! You've maintained a 5-day study streak without missing a beat."
  },
  {
    id: 3,
    emoji: '🏆',
    title: 'A1 Master',
    unlocked: true,
    achievedDate: 'Achieved Dec 01, 2023',
    description: 'Perfect score! You completed the A1 level assessment with 100% accuracy.'
  },
  {
    id: 4,
    emoji: '🚀',
    title: 'In Progress',
    unlocked: false,
    progress: 'Need 15 more pts',
    description: 'Complete 5 more advanced quizzes to launch into the next phase of your journey.'
  },
  {
    id: 5,
    emoji: '🤝',
    title: 'Social Butterfly',
    unlocked: false,
    progress: '2/5 Referrals',
    description: 'Invite more friends to join HackaEdu and earn exclusive collaborative rewards.'
  },
  {
    id: 6,
    emoji: '🦉',
    title: 'Night Owl',
    unlocked: false,
    progress: '0% Complete',
    description: 'Study for at least 1 hour after 10:00 PM to unlock this nocturnal badge.'
  }
])

const userLevel = ref(4)
const unlockedCount = ref(3)
const totalCount = ref(7)
</script>

<template>
  <div class="w-full px-4 sm:px-6 lg:px-8 py-6 sm:py-8">
    <!-- Header -->
    <AchievementsHeader 
      :level="userLevel"
      :unlocked-count="unlockedCount"
      :total-count="totalCount"
    />

    <!-- Achievements Grid -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4 sm:gap-5 lg:gap-6">
      <AchievementCard
        v-for="achievement in achievements"
        :key="achievement.id"
        :achievement="achievement"
      />
    </div>
  </div>
</template>

<template>
  <div class="restocking">
    <div class="page-header">
      <h2>{{ t('restocking.title') }}</h2>
      <p>{{ t('restocking.description') }}</p>
    </div>

    <div class="card">
      <form class="budget-form" @submit.prevent="fetchRecommendations">
        <div class="form-group">
          <label for="restocking-budget">{{ t('restocking.budgetLabel') }}</label>
          <input
            id="restocking-budget"
            v-model="budget"
            type="number"
            min="0"
            step="0.01"
            :placeholder="t('restocking.budgetPlaceholder')"
            class="budget-input"
          />
        </div>
        <button type="submit" class="submit-btn">{{ t('restocking.submitButton') }}</button>
      </form>
    </div>

    <div v-if="loading" class="loading">{{ t('common.loading') }}</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <template v-else-if="hasSearched && result">
      <div class="stats-grid">
        <StatCard :label="t('restocking.totalCost')" :value="formatCurrency(result.total_cost)" variant="info" />
        <StatCard :label="t('restocking.remainingBudget')" :value="formatCurrency(result.remaining_budget)" variant="success" />
        <StatCard :label="t('restocking.itemsRecommended')" :value="result.items_recommended" variant="neutral" />
        <StatCard :label="t('restocking.itemsNeedingRestock')" :value="result.items_needing_restock" variant="warning" />
      </div>

      <div v-if="recommendations.length === 0" class="card">
        <p class="empty-state">{{ t('restocking.noRecommendations') }}</p>
      </div>
      <div v-else class="card">
        <div class="card-header">
          <h3 class="card-title">{{ t('restocking.recommendationsTitle') }}</h3>
        </div>
        <div class="table-container">
          <table>
            <thead>
              <tr>
                <th>{{ t('restocking.table.sku') }}</th>
                <th>{{ t('restocking.table.itemName') }}</th>
                <th>{{ t('restocking.table.category') }}</th>
                <th>{{ t('restocking.table.quantityOnHand') }}</th>
                <th>{{ t('restocking.table.quantityToOrder') }}</th>
                <th>{{ t('restocking.table.unitCost') }}</th>
                <th>{{ t('restocking.table.lineTotal') }}</th>
                <th>{{ t('restocking.table.priority') }}</th>
                <th>{{ t('restocking.table.reason') }}</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in recommendations" :key="item.sku">
                <td><strong>{{ item.sku }}</strong></td>
                <td>{{ item.name }}</td>
                <td>{{ item.category }}</td>
                <td>{{ item.quantity_on_hand }}</td>
                <td>
                  <strong v-if="item.fully_funded">{{ item.quantity_to_order }}</strong>
                  <strong v-else>{{ item.quantity_to_order }} / {{ item.quantity_needed }}</strong>
                </td>
                <td>{{ formatCurrency(item.unit_cost) }}</td>
                <td>{{ formatCurrency(item.line_total) }}</td>
                <td>
                  <span class="badge" :class="item.priority">{{ t('priority.' + item.priority) }}</span>
                </td>
                <td>{{ item.priority_reason }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </template>
    <div v-else class="empty-state">{{ t('restocking.emptyPrompt') }}</div>
  </div>
</template>

<script>
import { ref, computed, watch } from 'vue'
import { api } from '../api'
import { useFilters } from '../composables/useFilters'
import { useI18n } from '../composables/useI18n'
import StatCard from '../components/StatCard.vue'

export default {
  name: 'Restocking',
  components: {
    StatCard
  },
  setup() {
    const { t } = useI18n()

    const budget = ref('')
    const loading = ref(false)
    const error = ref(null)
    const result = ref(null)
    const hasSearched = ref(false)

    const { selectedLocation, selectedCategory, getCurrentFilters } = useFilters()

    const recommendations = computed(() => result.value?.recommendations ?? [])

    const formatCurrency = (value) => {
      return Number(value).toLocaleString('en-US', { style: 'currency', currency: 'USD' })
    }

    const fetchRecommendations = async () => {
      if (!budget.value || Number(budget.value) <= 0) {
        error.value = t('restocking.invalidBudget')
        return
      }

      try {
        loading.value = true
        error.value = null
        hasSearched.value = true
        result.value = await api.getRestockingRecommendations(Number(budget.value), getCurrentFilters())
      } catch (err) {
        error.value = err.response?.data?.detail || t('common.error')
      } finally {
        loading.value = false
      }
    }

    watch([selectedLocation, selectedCategory], () => {
      if (hasSearched.value) {
        fetchRecommendations()
      }
    })

    return {
      t,
      budget,
      loading,
      error,
      result,
      hasSearched,
      recommendations,
      formatCurrency,
      fetchRecommendations
    }
  }
}
</script>

<style scoped>
.budget-form {
  display: flex;
  align-items: flex-end;
  gap: 1rem;
  flex-wrap: wrap;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group label {
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--color-text-secondary);
}

.budget-input {
  padding: 0.75rem;
  border: 2px solid var(--color-border);
  border-radius: var(--radius-md);
  font-size: 0.95rem;
  font-family: inherit;
  min-width: 220px;
  transition: border-color 0.2s ease;
}

.budget-input:focus {
  outline: none;
  border-color: var(--color-primary-600);
}

.submit-btn {
  padding: 0.75rem 1.75rem;
  background: linear-gradient(135deg, var(--color-primary-600) 0%, var(--color-primary-700) 100%);
  color: white;
  border: none;
  border-radius: var(--radius-md);
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s ease, opacity 0.2s ease;
  white-space: nowrap;
  height: fit-content;
}

.submit-btn:hover {
  transform: translateY(-2px);
}

.empty-state {
  text-align: center;
  padding: 3rem;
  color: var(--color-text-muted);
  font-size: 1rem;
}
</style>

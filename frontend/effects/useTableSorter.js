import { useState } from 'react'

export default function useTableSorter(initialKey) {
  const [sortAscending, setSortAscending] = useState(true)
  const [sortKey, setSortKey] = useState(initialKey)

  const onHeaderClick = () => newSortBy => {
    if (newSortBy === sortKey) {
      setSortAscending(currentSortAscending => !currentSortAscending)
    } else {
      setSortAscending(true)
      setSortKey(newSortBy)
    }
  }

  const getSortedItems = items =>
    [...items].sort(
      (itemA, itemB) =>
        itemA[sortKey].localeCompare(itemB[sortKey], undefined, {
          numeric: true,
        }) * (sortAscending ? 1 : -1),
    )

  return { getSortedItems, onHeaderClick }
}

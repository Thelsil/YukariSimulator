
class quickSort() :

    def __init__(self, listToSort,attributeName, VERBOSE = False):
        self.listToSort = listToSort.copy()
        self.attributeName = attributeName
        self.__VERBOSE = VERBOSE

    def __call__(self,k):
        if self.__VERBOSE:
            print("Before sort: " + str(self.listToSort))

        self.__sort(0, len(self.listToSort) - 1,k)

        if self.__VERBOSE:
            print("After sort: " + str(self.listToSort))

        return self.listToSort[k]


    def __getListValue(self,index):
        return getattr(self.listToSort[index], self.attributeName)

    def __swap(self, x, y):
        self.listToSort[x], self.listToSort[y] = self.listToSort[y], self.listToSort[x]

    def __sort(self, indexLeft, indexRight, k):
        if indexLeft >= indexRight:
            return

        pivotIndexes = self.__partition(indexLeft, indexRight)

        newIndexLeft = pivotIndexes[0]
        newIndexRight = pivotIndexes[1]

        if indexLeft < newIndexRight and k <= newIndexRight:
            self.__sort(indexLeft, newIndexRight, k)

        if newIndexLeft < indexRight and k <= newIndexLeft:
            self.__sort(newIndexLeft, indexRight, k)


    # The partition re-order a part of the list (a sub-list) between "indexLeft" and "indexRight".
    # This sub-list is divided into 2 groups around a pivot (located around at the middle of the sub-list).
    # Once re-ordered, any element of the group at the left of the pivot is inferior to any element at the right of the pivot
    # (but elements within each group are not necessary ordered.
    def __partition(self, indexLeft, indexRight):

        # Set the pivot value, located at the median index of the partition.
        pivot_index = int((indexLeft + indexRight) / 2)
        pivot_value = self.__getListValue( pivot_index )

        # Initialize the new indexes once the partition is processed.
        newIndexLeft = indexLeft
        newIndexRight = indexRight
        while 1:

            # Shift the left index until an element in the list is higher (or equals) to the pivot value.
            while newIndexLeft < indexRight and (self.__getListValue(newIndexLeft) < pivot_value):
                newIndexLeft += 1

            # Shift the right index until an element in the list is lower (or equals) to the pivot value.
            while newIndexRight > indexLeft and (self.__getListValue(newIndexRight) > pivot_value):
                newIndexRight -= 1

            # If the indexes are crossed, the partition is correctly re-ordered.
            if newIndexLeft > newIndexRight:
                return [newIndexLeft, newIndexRight]

            # Exchange the position of the elements.
            self.__swap(newIndexLeft, newIndexRight)

            # Increment indexes for the next iteration.
            newIndexLeft += 1
            newIndexRight -= 1

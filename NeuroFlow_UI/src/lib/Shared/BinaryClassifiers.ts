export const classifiers = {
    LogisticRegression: {
        params: ['C', 'max_iter'], // 'C' for regularization strength, 'solver' for the algorithm
    },
    SupportVectorMachine: {
        params: ['C', 'gamma'], // 'C' for regularization strength, 'kernel' for the kernel type
    },
    DecisionTrees: {
        params: ['max_depth', 'min_samples_split'], // 'max_depth' of the tree, 'min_samples_split' for the minimum number of samples required to split
    },
    RandomForest: {
        params: ['n_estimators', 'max_depth'], // 'n_estimators' for the number of trees, 'max_depth' of the tree
    },
};
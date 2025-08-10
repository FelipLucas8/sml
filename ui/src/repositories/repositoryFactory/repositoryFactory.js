import modelRepository from "../modelRepository";

const repositories = {
  models: modelRepository
};

export const RepositoryFactory = {
  get: (name) => repositories[name],
};
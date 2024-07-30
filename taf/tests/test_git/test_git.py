import pytest
import tempfile
from taf.exceptions import GitError
from taf.git import GitRepository


def test_clone_from_local(repository, clone_repository):
    clone_repository.clone_from_disk(repository.path)
    assert clone_repository.is_git_repository
    commits = clone_repository.all_commits_on_branch()
    assert len(commits)


def test_is_branch_with_unpushed_commits(repository, clone_repository):
    clone_repository.clone_from_disk(repository.path, keep_remote=True)
    branch = clone_repository.branches()[0]
    clone_repository.reset_num_of_commits(1, True)
    assert not clone_repository.is_branch_with_unpushed_commits(branch)
    (clone_repository.path / "test3.txt").write_text("Updated test3")
    clone_repository.commit(message="Update test3.txt")
    assert clone_repository.is_branch_with_unpushed_commits(branch)


def test_is_git_repository_root_bare(repository):
    repository.init_repo(bare=True)
    assert repository.is_git_repository
    assert repository.is_git_repository_root


def test_is_git_repository_root_non_bare(repository):
    repository.init_repo(bare=False)
    assert repository.is_git_repository
    assert repository.is_git_repository_root


def test_head_commit_sha():
    with tempfile.TemporaryDirectory() as tmpdirname:
        repo = GitRepository(path=tmpdirname)
        with pytest.raises(
            GitError,
            match=f"Repo {repo.name}: The path '{repo.path.as_posix()}' is not a Git repository.",
        ):
            repo.head_commit_sha() is not None


def test_create_delete_branch(repository):
    all_branches = repository.branches(all=True)
    print("Initial branches:", all_branches)

    default_branch = repository.get_default_branch()
    assert default_branch in all_branches, f"Default branch ({default_branch}) not found"  

    new_branch_name = "test_branch"
    repository.create_branch(new_branch_name)

    all_branches = repository.branches(all=True)
    print("Branches after creating a new branch:", all_branches)
    assert new_branch_name in all_branches, f"Branch {new_branch_name} was not created"
    
    repository.delete_branch(new_branch_name)

    all_branches = repository.branches(all=True)
    print("Branches after deleting the new branch:", all_branches)
    assert new_branch_name not in all_branches, f"Branch {new_branch_name} was not deleted"
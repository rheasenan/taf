import click
import taf.developer_tool as developer_tool
from taf.constants import DEFAULT_RSA_SIGNATURE_SCHEME
from taf.updater.updater import update_repository


def attach_to_group(group):

    @group.group()
    def repo():
        pass

    @repo.command()
    @click.argument("path")
    @click.option("--keys-description", help="A dictionary containing information about the "
                  "keys or a path to a json file which stores the needed information")
    @click.option("--keystore", default=None, help="Location of the keystore files")
    @click.option("--commit", is_flag=True, help="Indicates if the changes should be "
                  "committed automatically")
    @click.option("--test", is_flag=True, default=False, help="Indicates if the created repository "
                  "is a test authentication repository")
    def create(path, keys_description, keystore, commit, test):
        """
        Create a new authentication repository at the specified location by registering
        signing keys and generating initial metadata files. Information about the roles
        can be provided through a dictionary - either specified directly or contained
        by a .json file whose path is specified when calling this command. This allows
        definition of: \n
            - total number of keys per role \n
            - threshold of signatures per role \n
            - should keys of a role be on Yubikeys or should keystore files be used \n
            - scheme (the default scheme is rsa-pkcs1v15-sha256) \n

        For example:\n
        {\n
            "root": {\n
                "number": 3,\n
                "length": 2048,\n
                "passwords": ["password1", "password2", "password3"]\n
                "threshold": 2,\n
                "yubikey": true\n
            },\n
            "targets": {\n
                "length": 2048\n
            },\n
            "snapshot": {},\n
            "timestamp": {}\n
            }\n

        In cases when this dictionary is not specified, it is necessary to enter the needed
        information when asked to do so, or confirm that default values should be used.
        If keys should be stored in keystore files, it is possible to either use already generated
        keys (stored in keystore files located at the path specified using the keystore option),
        or to generate new one.

        If the test flag is set, a special target file will be created. This means that when
        calling the updater, it'll be necessary to use the --authenticate-test-repo flag.
        """
        developer_tool.create_repository(path, keystore, keys_description, commit, test)

    @repo.command()
    @click.argument("path")
    @click.option("--root-dir", default=None, help="Directory where target repositories and, "
                  "optionally, authentication repository are located. If omitted it is "
                  "calculated based on authentication repository's path. "
                  "Authentication repo is persumed to be at root-dir/namespace/auth-repo-name")
    @click.option("--namespace", default=None, help="Namespace of the target repositories. "
                  "If omitted, it will be assumed that namespace matches the name of the "
                  "directory which contains the authentication repository")
    @click.option("--targets-rel-dir", default=None, help="Directory relative to which "
                  "urls of the target repositories are calculated. Only useful when "
                  "the target repositories do not have remotes set")
    @click.option("--custom", default=None, help="A dictionary containing custom "
                  "targets info which will be added to repositories.json")
    def generate_repositories_json(path, root_dir, namespace, targets_rel_dir, custom):
        """
        Generate repositories.json. This file needs to be one of the authentication repository's
        target files or the updater won't be able to validate target repositories.
        repositories.json is generated by traversing through all targets and adding an entry
        with the namespace prefixed name of the target repository as its key and the
        repository's url and custom data as its value.

        Target repositories are expected to be inside a directory whose name is equal to the specified
        namespace and which is located inside the root directory. If root directory is E:\\examples\\root
        and namespace is namespace1, target repositories should be in E:\\examples\\root\\namespace1.
        If the authentication repository and the target repositories are in the same root directory and
        the authentication repository is also directly inside a namespace directory, then the common root
        directory is calculated as two repositories up from the authetication repository's directory.
        Authentication repository's namespace can, but does not have to be equal to the namespace of target,
        repositories. If the authentication repository's path is E:\\root\\namespace\\auth-repo, root
        directory will be determined as E:\\root. If this default value is not correct, it can be redefined
        through the --root-dir option. If the --namespace option's value is not provided, it is assumed
        that the namespace of target repositories is equal to the authentication repository's namespace,
        determined based on the repository's path. E.g. Namespace of E:\\root\\namespace2\\auth-repo
        is namespace2.

        The url of a repository corresponds to its git remote url if set and to its location on the file
        system otherwise. Test repositories might not have remotes. If targets-rel-dir is specified
        and a repository does not have remote url, its url is calculated as a relative path to the
        repository's location from this path.

        While urls are the only information that the updater needs, it is possible to add
        any other data using the custom option. Custom data can either be specified in a .json file
        whose path is provided when calling this command, or directly entered. Keys is this
        dictionary are names of the repositories whose custom data should be set and values are
        custom data dictionaries. For example:

        {\n
            "test/html-repo": {\n
                "type": "html"\n
            },
            "test/xml-repo": {\n
                "type": "xml"\n
            }\n
        }\n

        Note: this command does not automatically register repositories.json as a target file.
        It is recommended that the content of the file is reviewed before doing so manually.
        """
        developer_tool.generate_repositories_json(path, root_dir, namespace, targets_rel_dir, custom)

    @repo.command()
    @click.argument('path')
    @click.option("--root-dir", default=None, help="Directory where target repositories and, "
                  "optionally, authentication repository are located. If omitted it is "
                  "calculated based on authentication repository's path. "
                  "Authentication repo is persumed to be at root-dir/namespace/auth-repo-name")
    @click.option("--namespace", default=None, help="Namespace of the target repositories. "
                  "If omitted, it will be assumed that namespace matches the name of the "
                  "directory which contains the authentication repository")
    @click.option('--targets-rel-dir', default=None, help=' Directory relative to which urls '
                  'of the target repositories are set, if they do not have remote set')
    @click.option("--targets-rel-dir", default=None, help="Directory relative to which "
                  "urls of the target repositories are calculated. Only useful when "
                  "the target repositories do not have remotes set")
    @click.option("--custom", default=None, help="A dictionary containing custom "
                  "targets info which will be added to repositories.json")
    @click.option("--add-branch", default=False, is_flag=True, help="Whether to add name of "
                  "the current branch to target files")
    @click.option("--keystore", default=None, help="Location of the keystore files")
    @click.option("--keys-description", help="A dictionary containing information about the "
                  "keys or a path to a json file which stores the needed information")
    @click.option("--commit", is_flag=True, help="Indicates if the changes should be "
                  "committed automatically")
    @click.option("--test", is_flag=True, default=False, help="Indicates if the created repository "
                  "is a test authentication repository")
    @click.option('--scheme', default=DEFAULT_RSA_SIGNATURE_SCHEME, help='A signature scheme used for signing.')
    def initialize(path, root_dir, namespace, targets_rel_dir, custom, add_branch, keystore,
                   keys_description, commit, test, scheme):
        """
        Create and initialize a new authentication repository:\n
            1. Crete an authentication repository (generate initial metadata files)\n
            2. Commit initial metadata files if commit == True\n
            3. Add target files corresponding to target repositories\n
            4. Generate repositories.json\n
            5. Update metadata files\n
            6. Commit the changes if commit == True\n
        Combines create, generate_repositories_json, update_repos and targets sign commands.
        In order to have greater control over individual steps and be able to review files created
        in the initialization process, execute the mentioned commands separately.
        """
        developer_tool.init_repo(path, root_dir, namespace, targets_rel_dir, custom, add_branch,
                                 keystore, keys_description, commit, test, scheme)

    @repo.command()
    @click.argument("url")
    @click.argument("clients-auth-path")
    @click.option("--clients-root-dir", default=None, help="Directory where target repositories and, "
                  "optionally, authentication repository are located. If omitted it is "
                  "calculated based on authentication repository's path. "
                  "Authentication repo is persumed to be at root-dir/namespace/auth-repo-name")
    @click.option("--from-fs", is_flag=True, default=False, help="Indicates if the we want to clone a "
                  "repository from the filesystem")
    @click.option("--authenticate-test-repo", is_flag=True, help="Indicates that the authentication "
                  "repository is a test repository")
    def update(url, clients_auth_path, clients_root_dir, from_fs, authenticate_test_repo):
        """
        Update and validate local authentication repository and target repositories. Remote
        authentication's repository url needs to be specified when calling this command. If the
        authentication repository and the target repositories are in the same root repository,
        locations of the target repositories are calculated based on the authentication repository's
        path. If that is not the case, it is necessary to redefine this default value using the
        --clients-root-dir option. This means that if authentication repository's path is
        E:\\root\\namespace\\auth-repo, it will be assumed that E:\\root is the root direcotry
        if clients-root-dir is not specified.
        Names of target repositories (as defined in repositories.json) are appened to the root repository's
        path thus defining the location of each target repository. If names of target repositories
        are namespace/repo1, namespace/repo2 etc and the root directory is E:\\root, path of target
        repositories will be calculated as E:\\root\\namespace\\repo1, E:\\root\\namespace\\root2 etc.

        If remote repository's url is a file system path, it is necessary yo call this command with
        --from-fs flag so that url validation is skipped. When updating a test repository (one that has
        the "test" target file), use --authenticate-test-repo flag. An error will be raised
        if this flag is omitted in the mentioned case. Do not use this flag when validating a non-test
        repository as that will also result in an error.
        """
        update_repository(url, clients_auth_path, clients_root_dir, from_fs,
                          authenticate_test_repo)

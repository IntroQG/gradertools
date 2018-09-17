## Caching GitHub credentials in different platforms

On **Windows** you can do that on command prompt by running (see [help](https://help.github.com/articles/caching-your-github-password-in-git)):

```git config --global credential.helper wincred```

On **Mac** you can do that with credential-osxkeychain:

*Check that the tool exists*

```$ git credential-osxkeychain```

*Cache your credentials*

```$ git config --global credential.helper osxkeychain```

On **Linux**, you can store the credentials for certain time period only:

```git config --global credential.helper 'cache --timeout=3600'```
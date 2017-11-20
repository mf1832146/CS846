from git import Repo
import Mining
import unittest


class TestMining(unittest.TestCase):
 
    def setUp(self):
        self.repo = Repo("Data/android-async-http")
        self.commits = [ commit for commit in self.repo.iter_commits()]
        self.commit = self.commits[10]
        self.diffs = self.commit.tree.diff(self.commit.parents[0].tree)
        self.diff = self.diffs[0]

        self.assertEqual(self.diff.a_path,
            'library/src/main/java/com/loopj/android/http/AsyncHttpResponseHandler.java')
        self.assertEqual(self.diff.b_path,
            'library/src/main/java/com/loopj/android/http/AsyncHttpResponseHandler.java')
        self.assertEqual(self.commit.hexsha, '2a9b4ef7de68196945920de480880a2b7829ba2a')

        with open("a_blob.java", "wb") as f:
            f.write(self.diff.a_blob.data_stream.read())
    
        with open("b_blob.java", "wb") as f:
            f.write(self.diff.b_blob.data_stream.read())
 
    def test_GumTreeDiffFiles(self):
        changes = Mining._GumTreeDiffFiles()
        print(len(changes))
        self.assertTrue(len(changes) == 65, "GumTreeDiffFiles introduced an regression. Number of changes mismatch.")
 
    def test_seperateContextAndTarget(self):
        changes = Mining._GumTreeDiffFiles()
        target, change_context = Mining._seperateContextAndTarget(changes, 40)
        w_scope, w_dep = Mining._computeWeights(target, change_context[12])

        self.assertEqual(w_scope, 0.5)
        self.assertEqual(w_dep, 0.5)

    def test_seperateContextAndTarget2(self):
        changes = Mining._GumTreeDiffFiles()
        target, change_context = Mining._seperateContextAndTarget(changes, 20)
        w_scope, w_dep = Mining._computeWeights(target, change_context[2])

        self.assertEqual(w_scope, 1)
        self.assertEqual(w_dep, 1)

    def test_change_context(self):
        changes = Mining._GumTreeDiffFiles()
        target, change_context = Mining._seperateContextAndTarget(changes, 6)

        self.assertEqual(len(change_context), 6)

        self.assertIn("action", target)
        self.assertIn("at", target)
        self.assertIn("dependant id", target)
        self.assertIn("id", target)
        self.assertIn("immediate scope", target)
        self.assertIn("label", target)
        self.assertIn("label string", target)
        self.assertIn("parent", target)
        self.assertIn("parent type", target)
        self.assertIn("pos", target)
        self.assertIn("tree", target)
        self.assertIn("type", target)

        self.assertEqual(target["action"], "insert")
        self.assertEqual(target["at"], 1)
        self.assertEqual(target["dependant id"], "SimpleName: Utils")
        self.assertEqual(target["id"], 377)
        self.assertEqual(target["immediate scope"], 404)
        self.assertEqual(target["label"], 'SimpleName: asserts')
        self.assertEqual(target["label string"], "asserts")
        self.assertEqual(target["parent"], 382)
        self.assertEqual(target["parent type"], 32)
        self.assertEqual(target["pos"], 5164)
        self.assertEqual(target["tree"], 377)
        self.assertEqual(target["type"], 42)

    def test_getNearbyTokens(self):
        tokens = Mining._getNearbyTokens({"pos": 4885})
        self.assertEqual(len(tokens), Mining.MAXIMUM_DEPTH)

        for token in tokens:
            self.assertEqual(token["typeLabel"], "SimpleName")

    def test_seperateContextAndTarget(self):
        changes = Mining._GumTreeDiffFiles()
        target, change_context = Mining._seperateContextAndTarget(changes, 6)

        last_change = change_context[-1]

        self.assertEqual(last_change["action"], "insert")
        self.assertEqual(last_change["at"], 0)
        self.assertEqual(last_change["dependant id"], "SimpleName: Utils")
        self.assertEqual(last_change["id"], 376)
        self.assertEqual(last_change["immediate scope"], 404)
        self.assertEqual(last_change["label"], 'SimpleName: Utils')
        self.assertEqual(last_change["label string"], "Utils")
        self.assertEqual(last_change["parent"], 382)
        self.assertEqual(last_change["parent type"], 32)
        self.assertEqual(last_change["pos"], 5158)
        self.assertEqual(last_change["tree"], 376)
        self.assertEqual(last_change["type"], 42)

    def test_make_sure_change_context_are_ascending(self):
        changes = Mining._GumTreeDiffFiles()
        target, change_context = Mining._seperateContextAndTarget(changes, 6)
        for i in range(len(change_context)-1):
            self.assertTrue(change_context[i]["pos"] <= change_context[i+1]["pos"]) 



if __name__ == '__main__':
    unittest.main()